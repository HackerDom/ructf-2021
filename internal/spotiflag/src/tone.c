#include <stdio.h>
#include <stdlib.h>

#include "tone.h"
#include "config.h"


void tone_init(tone_t *tone, tone_value_t start, tone_value_t end, tone_value_t frequency) {
    if (tone->is_initialized) {
        return;
    }

    vector_init(&tone->values, NULL);

    tone->start = start;
    tone->end = end;
    tone->frequency = frequency;

    tone->is_initialized = true;
    tone->is_finalized = false;
}

void tone_clear(tone_t *tone) {
    if (!tone->is_initialized) {
        return;
    }

    vector_clear(&tone->values);

    tone->is_initialized = false;
    tone->is_finalized = false;
}

void tone_finalize(tone_t *tone) {
    if (!tone->is_initialized || tone->is_finalized) {
        return;
    }

    tone_value_t tone_duration = tone->end - tone->start;
    size_t values_count = (size_t)(tone_duration * WAV_SAMPLE_RATE) + 1;

    tone_value_t step = 2 * M_PIq * tone->frequency / WAV_SAMPLE_RATE;

    for (size_t i = 0; i < values_count; i++) {
        tone_value_t *value = calloc(1, sizeof(tone_value_t));

        if (value == NULL) {
            perror("calloc error");
            exit(1);
        }

        *value = sinq(i * step) * WAV_AMPLITUDE_LIMIT;

        vector_append(&tone->values, value);
    }

    tone->is_finalized = true;
}
