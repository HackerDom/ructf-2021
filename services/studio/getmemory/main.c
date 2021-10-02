#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>

unsigned char *mx_hmac_sha256(const void *key, int keylen,
                              const unsigned char *data, int datalen,
                              unsigned char *result, unsigned int *resultlen) {
    return HMAC(EVP_sha256(), key, keylen, data, datalen, result, resultlen);
}

void print_buffer(const char* buffer, unsigned long long length)
{
    const int REGULARPACKAGE_SIZE = 4096;
    unsigned long bytesWritten;                   /* Bytes written so far in the buffer */
    int bytesToWrite;                             /* Bytes to write to file */
    char *tmpBuffer;                              /* Temporary buffer */

    bytesWritten = 0;

    while ( bytesWritten < length )
    {
        if ( length - bytesWritten >= REGULARPACKAGE_SIZE )  /* not last frame */
        {
            bytesToWrite = REGULARPACKAGE_SIZE;
        }
        else                                                 /* last frame */
        {
            bytesToWrite = length - bytesWritten;
            // reallocate tmpBuffer to its adecuate size
        }
        // copy original buffer <bytesToWrite> elements to tmpBuffer
        tmpBuffer = &buffer[bytesWritten];
        // write tmpBuffer to file
        fwrite ( tmpBuffer , 1 , bytesToWrite , stdout );
        fflush(stdout);
        // just upgrade the var
        bytesWritten += bytesToWrite;
    }
}

char *
hex2str(const unsigned char * hex, int hex_len)
{
        char *str = malloc(2*hex_len + 1);
    if (!str) {
            printf("OH SHIT");
            fflush(stdout);
        return NULL;
    }

    char * ptr = str;
    const unsigned char * hptr = hex;

    const char hex_digit[] = {
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
    };

    for (int ct = 0; ct < hex_len; ct++, hptr++) {
        *ptr++ = hex_digit[*hptr >> 4];
        *ptr++ = hex_digit[*hptr & 0x0f];
    }

    *ptr = '\0';
    return str;
}

int create_key(long long job_id, char * key_path, char ** key) {
    struct stat secret_st;
    int secret_fd;
    void *secret_addr;

    int job_id_len;
    char *job_id_str;

    unsigned char *key_bytes = NULL;
    unsigned int key_bytes_len = 0;

    if ((secret_fd = open(key_path, O_RDONLY, S_IRUSR)) < 0)
    {
        perror("Error in private key file opening");
        return EXIT_FAILURE;
    }

    if (fstat(secret_fd, &secret_st) < 0)
    {
        perror("Error in fstat");
        return EXIT_FAILURE;
    }

    secret_addr = mmap(NULL, secret_st.st_size, PROT_READ, MAP_SHARED, secret_fd, 0);
    if (secret_addr == MAP_FAILED)
    {
        perror("mmap");
        return 30;
    }

    // convert job_id to str
    job_id_len = snprintf(NULL, 0, "%lld", job_id);
    job_id_str = malloc( job_id_len + 1 );
    snprintf(job_id_str, job_id_len + 1, "%lld", job_id);


    key_bytes = mx_hmac_sha256((const void *)secret_addr, secret_st.st_size, (unsigned char*)job_id_str, job_id_len + 1, key_bytes, &key_bytes_len);

    *key = hex2str(key_bytes, key_bytes_len);
    return 0;
}


int main_internal(long long file_id, char * key_path)
{
    int fd, rc;
    char *key;
    uint64_t res_size;
    void *addr;

    rc = create_key(file_id, key_path, &key);
    if (rc != 0) {
        perror("create_key_fail");
        return rc;
    }

    fd = shm_open(key, O_RDONLY, S_IRUSR | S_IWUSR);
    if (fd == -1)
    {
        perror("open");
        return 10;
    }

    //read header at first
    addr = mmap(NULL, sizeof(uint64_t), PROT_READ, MAP_SHARED, fd, 0);
    if (addr == MAP_FAILED)
    {
        perror("mmap");
        return 30;
    }

    memcpy(&res_size, addr, sizeof(uint64_t));

    rc = munmap(addr, sizeof(uint64_t));
    if (rc == -1)
    {
        perror("munmap");
        return 40;
    }

    addr = mmap(NULL, res_size + sizeof(uint64_t), PROT_READ, MAP_SHARED, fd, 0);
    if (addr == MAP_FAILED)
    {
        perror("mmap");
        return 30;
    }

    //sleep(9999999);
   
    print_buffer(addr + sizeof(uint64_t), res_size);

    rc = munmap(addr, res_size + sizeof(uint64_t));
    if (rc == -1)
    {
        perror("munmap");
        return 40;
    }

    return 0;
}

int main(int argc, char *argv[]) {
    if(argc<=2) {         printf("usage: [bin] job_id /path/to/key\n");         exit(1);      }
    int job_id = atoi(argv[1]);
    main_internal(job_id, argv[2]);

    return 0;
}
