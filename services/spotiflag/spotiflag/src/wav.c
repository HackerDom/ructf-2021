#include <stdlib.h>

#include "wav.h"
#include "frame.h"
#include "config.h"


void wav_init(wav_t *wav) {
    if (wav->is_initialized) {
        return;
    }

    vector_init(&wav->channels, &channel_clear);
    vector_init(&wav->frames, &frame_clear);

    wav->is_initialized = true;
    wav->is_finalized = false;
}

void wav_clear(wav_t *wav) {
    if (!wav->is_initialized) {
        return;
    }

    vector_clear(&wav->frames);
    vector_clear(&wav->channels);

    wav->is_initialized = false;
    wav->is_finalized = false;
}

void wav_add_channel(wav_t *wav, channel_t *channel) {
    if (!wav->is_initialized || wav->is_finalized) {
        return;
    }

    vector_append(&wav->channels, channel);
}

void wav_finalize_header(wav_t *wav) {
    wav->header.subchunk2_size = wav->channels.size * wav->frames.size * sizeof(frame_value_t);
    wav->header.subchunk2_id = 0x61746164;

    wav->header.num_channels = wav->channels.size;
    wav->header.bits_per_sample = 16;
    wav->header.block_align = wav->header.num_channels * wav->header.bits_per_sample / 8;
    wav->header.sample_rate = WAV_SAMPLE_RATE;
    wav->header.byte_rate = wav->header.sample_rate * wav->header.block_align;
    wav->header.audio_format = 1;
    wav->header.subchunk1_size = 16;
    wav->header.subchunk1_id = 0x20746d66;

    wav->header.format = 0x45564157;
    wav->header.chunk_size = wav->header.subchunk2_size + sizeof(wav_header_t) - sizeof(int32_t) - sizeof(int32_t);
    wav->header.chunk_id = 0x46464952;
}

void wav_finalize(wav_t *wav) {
    if (!wav->is_initialized || wav->is_finalized) {
        return;
    }

    wav->length = 0;

    size_t frames_count = 0;

    for (size_t i = 0; i < wav->channels.size; i++) {
        channel_t *channel = vector_get(&wav->channels, i);

        channel_finalize(channel);

        if (channel->values.size > frames_count) {
            frames_count = channel->values.size;
        }
    }

    for (size_t i = 0; i < frames_count; i++) {
        frame_t *frame = calloc(1, sizeof(frame_t));

        if (frame == NULL) {
            perror("calloc error");
            exit(1);
        }

        frame_init(frame);

        for (size_t k = 0; k < wav->channels.size; k++) {
            channel_t *channel = vector_get(&wav->channels, k);
            frame_value_t *frame_value = calloc(1, sizeof(frame_value_t));

            if (frame_value == NULL) {
                perror("calloc error");
                exit(1);
            }

            if (i < channel->values.size) {
                *frame_value = *((frame_value_t *)vector_get(&channel->values, i));
            }
            else {
                *frame_value = 0;
            }

            frame_add_value(frame, frame_value);

            wav->length += sizeof(frame_value_t);
        }

        vector_append(&wav->frames, frame);
    }

    wav_finalize_header(wav);

    wav->length += sizeof(wav_header_t);

    wav->is_finalized = true;
}

void wav_write(wav_t *wav, FILE *file) {
    if (!wav->is_finalized) {
        return;
    }

    fwrite(&wav->header, sizeof(wav_header_t), 1, file);

    for (size_t i = 0; i < wav->frames.size; i++) {
        frame_t *frame = vector_get(&wav->frames, i);

        for (size_t k = 0; k < frame->values.size; k++) {
            frame_value_t *frame_value = vector_get(&frame->values, k);

            fwrite(frame_value, sizeof(frame_value_t), 1, file);
        }
    }
}
