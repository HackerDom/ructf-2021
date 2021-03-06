#ifndef _CONFIG_H
#define _CONFIG_H

#include <stdint.h>


enum { 
    WAV_SAMPLE_RATE = 3000,
    WAV_AMPLITUDE_LIMIT = 16384,

    RANDOM_BITS = 128,
    RANDOM_STATE_SIZE = 32,

    SONG_SECONDS = 60,
    SONG_TONE_BITS = 10,
    SONG_TONE_SPEED = 4,
    SONG_TONE_DISTANCE = 1,
    SONG_BASE_FREQUENCY = 256,
    SONG_CHANNELS_COUNT = 2,

    CHUNK_SIZE = 64 * 1024,
};


#endif
