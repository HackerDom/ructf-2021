#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/socket.h>

#include "server.h"


void server_init(server_t *server, char *path) {
    if (server->is_initialized) {
        return;
    }

    signal(SIGCHLD, SIG_IGN);

    server->addr.sun_family = AF_UNIX;

    strncpy(server->addr.sun_path, path, sizeof(server->addr.sun_path));

    server->is_initialized = true;
}

void server_clear(server_t *server) {
    if (!server->is_initialized) {
        return;
    }

    close(server->fd);
    unlink(server->addr.sun_path);

    server->is_initialized = false;
}

void server_run(server_t *server, server_handler_t handler) {
    if (!server->is_initialized) {
        return;
    }

    server->fd = socket(AF_UNIX, SOCK_STREAM, 0);

    if (server->fd < 0) {
        perror("socket error");
        exit(1);
    }

    if (bind(server->fd, &server->addr, sizeof(struct sockaddr_un)) < 0) {
        perror("bind error");
        exit(1);
    }

    if (listen(server->fd, 1024) < 0) {
        perror("listen error");
        exit(1);
    }

    while (true) {
        int client = accept(server->fd, NULL, 0);

        if (client < 0) {
            perror("accept error");
            exit(1);
        }

        int pid = fork();

        if (pid < 0) {
            perror("fork error");
            exit(1);
        }
        else if (pid == 0) {
            close(server->fd);

            handler(client);
            close(client);

            _Exit(0);
        }
        else {
            close(client);
        }
    }
}
