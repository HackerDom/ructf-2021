#ifndef _MIXER_H
#define _MIXER_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "wav.h"
#include "tone.h"
#include "vector.h"


typedef struct mixer_s {
    bool is_initialized;
    bool is_finalized;
    wav_t wav;
} mixer_t;

void mixer_init(mixer_t *mixer);

void mixer_clear(mixer_t *mixer);

void mixer_add_tone(mixer_t *mixer, size_t channel_number, tone_value_t start, tone_value_t end, tone_value_t frequency);

void mixer_finalize(mixer_t *mixer);

void mixer_write_wav(mixer_t *mixer, FILE *file);


#endif
