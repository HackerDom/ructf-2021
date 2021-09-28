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

#define STORAGE_SIZE 8192

unsigned char *mx_hmac_sha256(const void *key, int keylen,
                              const unsigned char *data, int datalen,
                              unsigned char *result, unsigned int *resultlen) {
    return HMAC(EVP_sha256(), key, keylen, data, datalen, result, resultlen);
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

int main(int argc, char *argv[]) {
    int fd, rc;
    long long job_id;
    char *key;

    if(argc<=2) {         printf("usage: [bin] job_id /path/to/key\n");         exit(1);      }
    job_id = atoll(argv[1]);

    rc = create_key(job_id, argv[2], &key);
    if (rc != 0) {
        perror("create_key");
        return rc;
    }

    printf("%s", key);
    fflush(stdout);

    // get shared memory file descriptor
    fd = shm_open(key, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);
    if (fd == -1)
    {
        perror("open");
        return 10;
    }

    // extend shared memory object as by default it's initialized with size 0
    rc = ftruncate(fd, STORAGE_SIZE);
    if (rc == -1)
    {
        perror("ftruncate");
        return 20;
    }

    return 0;
}
