#ifndef _RANDOM_H
#define _RANDOM_H

#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

#include "config.h"


typedef __uint128_t random_element_t;

typedef struct random_s {
    bool is_initialized;
    size_t index;
    size_t element_index;
    random_element_t state[RANDOM_STATE_SIZE];
} random_t;

void random_init(random_t *random, uint8_t *seed_data, size_t seed_length);

void random_clear(random_t *random);

random_element_t random_next(random_t *random, size_t bits);


#endif
