#include <stdio.h>
#include <stdlib.h>

#include "channel.h"
#include "config.h"
#include "frame.h"


void channel_init(channel_t *channel) {
    if (channel->is_initialized) {
        return;
    }

    vector_init(&channel->tones, &tone_clear);
    vector_init(&channel->values, NULL);

    channel->is_initialized = true;
    channel->is_finalized = false;
}

void channel_clear(channel_t *channel) {
    if (!channel->is_initialized) {
        return;
    }

    vector_clear(&channel->tones);
    vector_clear(&channel->values);

    channel->is_initialized = false;
    channel->is_finalized = false;
}

void channel_add_tone(channel_t *channel, tone_t *tone) {
    if (!channel->is_initialized || channel->is_finalized) {
        return;
    }

    vector_append(&channel->tones, tone);
}

void channel_finalize(channel_t *channel) {
    if (!channel->is_initialized || channel->is_finalized) {
        return;
    }

    tone_value_t channel_duration = 0;

    for (size_t i = 0; i < channel->tones.size; i++) {
        tone_t *tone = vector_get(&channel->tones, i);

        tone_finalize(tone);

        if (tone->end > channel_duration) {
            channel_duration = tone->end;
        }
    }

    size_t channel_frames_count = (size_t)(channel_duration * WAV_SAMPLE_RATE) + 1;

    vector_t frame_values_counts = { 0 };
    vector_init(&frame_values_counts, NULL);

    for (size_t i = 0; i < channel_frames_count; i++) {
        frame_value_t *frame_value = calloc(1, sizeof(frame_value_t));

        if (frame_value == NULL) {
            perror("calloc error");
            exit(1);
        }

        vector_append(&channel->values, frame_value);

        size_t *frame_values_count = calloc(1, sizeof(size_t));

        if (frame_values_count == NULL) {
            perror("calloc error");
            exit(1);
        }

        vector_append(&frame_values_counts, frame_values_count);
    }

    for (size_t i = 0; i < channel->tones.size; i++) {
        tone_t *tone = vector_get(&channel->tones, i);

        size_t start_frame_index = tone->start * WAV_SAMPLE_RATE;
        size_t end_frame_index = tone->end * WAV_SAMPLE_RATE;

        for (size_t k = 0; k < tone->values.size; k++) {
            size_t frame_index = k + start_frame_index;

            tone_value_t *tone_value = vector_get(&tone->values, k);
            frame_value_t *frame_value = vector_get(&channel->values, frame_index);

            *frame_value += *tone_value;

            size_t *frame_values_count = vector_get(&frame_values_counts, frame_index);

            *frame_values_count += 1;
        }
    }

    for (size_t i = 0; i < channel_frames_count; i++) {
        frame_value_t *frame_value = vector_get(&channel->values, i);
        size_t *frame_values_count = vector_get(&frame_values_counts, i);

        if (frame_values_count > 0) {
            *frame_value /= *frame_values_count;
        }
    }

    vector_clear(&frame_values_counts);

    /* O(n^2)
    for (size_t i = 0; i < channel_frames_count; i++) {
        tone_value_t value = 0;
        size_t tones_count = 0;

        for (size_t k = 0; k < channel->tones.size; k++) {
            tone_t *tone = vector_get(&channel->tones, k);

            size_t start_frame_index = tone->start * WAV_SAMPLE_RATE;
            size_t end_frame_index = tone->end * WAV_SAMPLE_RATE;

            if (i >= start_frame_index && i < end_frame_index) {
                tone_value_t *tone_value = vector_get(&tone->values, i - start_frame_index);
                value += *tone_value;
                tones_count += 1;
            }
        }

        value /= tones_count;

        frame_value_t *frame_value = calloc(1, sizeof(frame_value_t));

        if (frame_value == NULL) {
            perror("calloc error");
            exit(1);
        }
        *frame_value = (frame_value_t)value;

        vector_append(&channel->values, frame_value);
    }
    */

    channel->is_finalized = true;
}
