#ifndef _FRAME_H
#define _FRAME_H

#include <stdint.h>
#include <stdbool.h>

#include "vector.h"


typedef int16_t frame_value_t;

typedef struct frame_s {
    bool is_initialized;
    vector_t values;
} frame_t;

void frame_init(frame_t *frame);

void frame_clear(frame_t *frame);

void frame_add_value(frame_t *frame, frame_value_t *frame_value);


#endif
