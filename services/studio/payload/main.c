#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#define STORAGE_SIZE 320000

int main(int argc, char *argv[]) {
    int fd;
    size_t len;
    void * addr;
    void * p;

    if(argc<=1) {         printf("usage: [bin] mem_id\n");         exit(1);      }


    // get shared memory file descriptor
    fd = shm_open(argv[1], O_RDWR, S_IWUSR);
    if (fd == -1)
    {
        perror("open");
        return 10;
    }

    char * to_write = "abc2";

    // map shared memory to process address space
    addr = mmap(NULL, STORAGE_SIZE, PROT_WRITE, MAP_SHARED, fd, 0);
    if (addr == MAP_FAILED)
    {
        perror("mmap");
        return 30;
    }

    p = addr;
    len = strlen(to_write);

    //write the length of the message to the header
    memcpy(p, &len, sizeof(size_t));
    p += sizeof(size_t);
    //write the data to the memory
    memcpy(p, to_write, len);

    return 0;
}
