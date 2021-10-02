#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <bits/sigaction.h>

#include "mixer.h"
#include "random.h"


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

    fwrite(&mixer.wav.length, sizeof(size_t), 1, wavfile);
    mixer_write_wav(&mixer, wavfile);

    mixer_clear(&mixer);
    random_clear(&random);
}


int main(int argc, char **argv, char **envp) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    size_t description_length;
    fread(&description_length, sizeof(size_t), 1, stdin);

    uint8_t description[description_length];
    memset(&description, 0, description_length);
    fread(&description, sizeof(uint8_t), description_length, stdin);

    song_generate(&description, description_length, stdout);

    return 0;
}
