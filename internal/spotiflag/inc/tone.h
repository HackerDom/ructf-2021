#ifndef _TONE_H
#define _TONE_H

#include <stdbool.h>
#include <quadmath.h>

#include "vector.h"


typedef __float128 tone_value_t;

typedef struct tone_s {
    bool is_initialized;
    bool is_finalized;
    tone_value_t start;
    tone_value_t end;
    tone_value_t frequency;
    vector_t values;
} tone_t;

void tone_init(tone_t *tone, tone_value_t start, tone_value_t end, tone_value_t frequency);

void tone_clear(tone_t *tone);

void tone_finalize(tone_t *tone);


#endif
