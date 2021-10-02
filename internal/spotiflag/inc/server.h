#ifndef _SERVER_H
#define _SERVER_H

#include <stdint.h>
#include <stdbool.h>
#include <sys/un.h>


typedef void (*server_handler_t)(int);

typedef struct server_s {
    bool is_initialized;
    int fd;
    struct sockaddr_un addr;
} server_t;

void server_init(server_t *server, char *path);

void server_clear(server_t *server);

void server_run(server_t *server, server_handler_t handler);


#endif
