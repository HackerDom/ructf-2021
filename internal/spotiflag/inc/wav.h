#ifndef _WAV_H
#define _WAV_H

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#include "vector.h"
#include "channel.h"


typedef struct wav_header_s {
    int32_t chunk_id;
    int32_t chunk_size;
    int32_t format;

    int32_t subchunk1_id;
    int32_t subchunk1_size;
    int16_t audio_format;
    int16_t num_channels;
    int32_t sample_rate;
    int32_t byte_rate;
    int16_t block_align;
    int16_t bits_per_sample;

    int32_t subchunk2_id;
    int32_t subchunk2_size;
} wav_header_t;

typedef struct wav_s {
    bool is_initialized;
    bool is_finalized;
    wav_header_t header;
    vector_t channels;
    vector_t frames;
    size_t length;
} wav_t;

void wav_init(wav_t *wav);

void wav_clear(wav_t *wav);

void wav_add_channel(wav_t *wav, channel_t *channel);

void wav_finalize(wav_t *wav);

void wav_write(wav_t *wav, FILE *file);


#endif
