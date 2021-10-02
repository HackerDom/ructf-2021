#include <stdlib.h>

#include "frame.h"


void frame_init(frame_t *frame) {
    if (frame->is_initialized) {
        return;
    }

    vector_init(&frame->values, NULL);

    frame->is_initialized = true;
}

void frame_clear(frame_t *frame) {
    if (!frame->is_initialized) {
        return;
    }

    vector_clear(&frame->values);

    frame->is_initialized = false;
}

void frame_add_value(frame_t *frame, frame_value_t *frame_value) {
    if (!frame->is_initialized) {
        return;
    }

    vector_append(&frame->values, frame_value);
}
