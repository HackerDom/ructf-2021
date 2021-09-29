#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#define STORAGE_SIZE 320000

int main(int argc, char *argv[]) {
    int fd, len;
    void * addr;

    if(argc<=1) {         printf("usage: [bin] mem_id\n");         exit(1);      }


    // get shared memory file descriptor
    fd = shm_open(argv[1], O_RDWR, S_IWUSR);
    if (fd == -1)
    {
        perror("open");
        return 10;
    }

    char * to_write = "abc";

    // map shared memory to process address space
    addr = mmap(NULL, STORAGE_SIZE, PROT_WRITE, MAP_SHARED, fd, 0);
    if (addr == MAP_FAILED)
    {
        perror("mmap");
        return 30;
    }

    // place data into memory
    len = strlen(to_write);
    memcpy(addr, to_write, len);

    return 0;
}
