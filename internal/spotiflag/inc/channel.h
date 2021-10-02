#ifndef _CHANNEL_H
#define _CHANNEL_H

#include <stdbool.h>

#include "tone.h"
#include "vector.h"


typedef struct channel_s {
    bool is_initialized;
    bool is_finalized;
    vector_t tones;
    vector_t values;
} channel_t;

void channel_init(channel_t *channel);

void channel_clear(channel_t *channel);

void channel_add_tone(channel_t *channel, tone_t *tone);

void channel_finalize(channel_t *channel);


#endif
