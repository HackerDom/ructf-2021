#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <bits/sigaction.h>

#include "mixer.h"
#include "random.h"
#include "server.h"


server_t server = { 0 };


void cleanup() {
    server_clear(&server);
}


void song_generate(uint8_t *description, size_t description_length, FILE *wavfile) {
    random_t random = { 0 };
    random_init(&random, description, description_length);

    mixer_t mixer = { 0 };
    mixer_init(&mixer);

    size_t length = (size_t)(SONG_SECONDS * SONG_TONE_SPEED) + 1;

    for (size_t channel = 0; channel < SONG_CHANNELS_COUNT; channel++) {
        for (size_t i = 0; i < length; i++) {
            random_element_t value = random_next(&random, SONG_TONE_BITS);

            tone_value_t tone_start = (tone_value_t)i / SONG_TONE_SPEED;
            tone_value_t tone_end = tone_start + (tone_value_t)1 / SONG_TONE_SPEED;
            tone_value_t tone_frequency = SONG_BASE_FREQUENCY + (tone_value_t)value * SONG_TONE_DISTANCE;

            mixer_add_tone(&mixer, channel, tone_start, tone_end, tone_frequency);
        }
    }

    mixer_finalize(&mixer);
    mixer_write_wav(&mixer, wavfile);

    mixer_clear(&mixer);
    random_clear(&random);
}


void song_generate_handler(FILE *io, char *wavfile_path) {
    size_t description_length;
    fread(&description_length, sizeof(size_t), 1, io);

    uint8_t description[description_length];
    memset(&description, 0, description_length);
    fread(&description, sizeof(uint8_t), description_length, io);

    FILE *wavfile = fopen(wavfile_path, "w");

    if (wavfile == NULL) {
        perror("fopen error");
        exit(1);
    }

    song_generate(&description, description_length, wavfile);

    fflush(wavfile);
    fclose(wavfile);
}


void song_read_handler(FILE *io, char *wavfile_path) {
    size_t offset;
    fread(&offset, sizeof(size_t), 1, io);

    FILE *wavfile = fopen(wavfile_path, "r");

    if (wavfile == NULL) {
        fwrite("NOTFOUND", sizeof(char), 8, io);
        return;
    }

    fseek(wavfile, offset, SEEK_SET);

    uint8_t buffer[CHUNK_SIZE];
    memset(&buffer, 0, CHUNK_SIZE);

    size_t size = fread(&buffer, sizeof(uint8_t), CHUNK_SIZE, wavfile);

    fwrite(&size, sizeof(size_t), 1, io);
    fwrite(&buffer, sizeof(uint8_t), size, io);

    fclose(wavfile);
}


void handler(int client) {
    FILE* io = fdopen(client, "r+");

    size_t id_length;
    fread(&id_length, sizeof(size_t), 1, io);

    char id[id_length];
    memset(&id, 0, id_length);
    fread(&id, sizeof(uint8_t), id_length, io);

    char *folder = "/tmp/songs/";
    char *format = "wav";

    size_t path_length = strlen(folder) + 1 + id_length + 1 + strlen(format) + 1;

    char path[path_length];
    memset(&path, 0, path_length);

    snprintf(&path, path_length, "%s/%s.%s", folder, id, format);

    uint64_t command;
    fread(&command, sizeof(uint64_t), 1, io);

    switch (command)
    {
        case 0x45544152454e4547: // GENERATE
            song_generate_handler(io, &path);
            break;

        case 0x4441455244414552: // READREAD
            song_read_handler(io, &path);
            break;

        default:
            fwrite("NOCOMMND", sizeof(char), 8, io);
            break;
    }

    fflush(io);
    fclose(io);
    close(client);
}


int main(int argc, char **argv, char **envp) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    atexit(cleanup);

    struct sigaction action = { 0 };
    action.sa_handler = &exit;

    sigaction(SIGINT, &action, NULL);
    sigaction(SIGTERM, &action, NULL);

    server_init(&server, "/tmp/spotiflag/spotiflag.sock");

    server_run(&server, handler);
}
