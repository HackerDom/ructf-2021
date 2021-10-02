#include <stdio.h>

#include "mixer.h"


void mixer_init(mixer_t *mixer) {
    if (mixer->is_initialized) {
        return;
    }

    wav_init(&mixer->wav);

    mixer->is_initialized = true;
    mixer->is_finalized = false;
}

void mixer_clear(mixer_t *mixer) {
    if (!mixer->is_initialized) {
        return;
    }

    wav_clear(&mixer->wav);

    mixer->is_initialized = false;
    mixer->is_finalized = false;
}

void mixer_add_tone(mixer_t *mixer, size_t channel_number, tone_value_t start, tone_value_t end, tone_value_t frequency) {
    if (!mixer->is_initialized || mixer->is_finalized) {
        return;
    }

    while (channel_number >= mixer->wav.channels.size) {
        channel_t *channel = calloc(1, sizeof(channel_t));

        if (channel == NULL) {
            perror("calloc error");
            exit(1);
        }

        channel_init(channel);

        vector_append(&mixer->wav.channels, channel);
    }

    channel_t *channel = vector_get(&mixer->wav.channels, channel_number);

    tone_t *tone = calloc(1, sizeof(tone_t));

    if (tone == NULL) {
        perror("calloc error");
        exit(1);
    }

    tone_init(tone, start, end, frequency);

    channel_add_tone(channel, tone);
}

void mixer_finalize(mixer_t *mixer) {
    if (!mixer->is_initialized || mixer->is_finalized) {
        return;
    }

    wav_finalize(&mixer->wav);

    mixer->is_finalized = true;
}

void mixer_write_wav(mixer_t *mixer, FILE *file) {
    if (!mixer->is_finalized) {
        return;
    }

    wav_write(&mixer->wav, file);
}
