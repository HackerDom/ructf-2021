#include "random.h"

#define TO_UINT128(X, Y) ((((__uint128_t)X) << 64) | ((__uint128_t)Y))
#define MAX(X, Y) (X > Y ? X : Y)
#define MIN(X, Y) (X < Y ? X : Y)


void memfrob(uint8_t *data, size_t size) {
    uint8_t xor, value;

    xor = 0;
    value = 1;

    for (size_t i = 0; i < size; i++) {
        data[size - i - 1] ^= value;
        xor ^= data[size - i - 1];
        value = (value * 11) % 251;
    }
}

void random_init_by_value(random_t *random, random_element_t seed_value) {
    const random_element_t MULTIPLIER = TO_UINT128(0x47f764020313fb98, 0x2e74d56c083cfbbb);

    random->state[0] = seed_value;

    for (size_t i = 1; i < RANDOM_STATE_SIZE; i++) {
        random->state[i] = MULTIPLIER * (random->state[i - 1] ^ (random->state[i - 1] >> (RANDOM_BITS - 2))) + i;
    }
}

void random_init_by_array(random_t *random, random_element_t *seed_array, size_t seed_array_length) {
    const random_element_t MULTIPLIER1 = TO_UINT128(0x9236e30df91d984e, 0x7c3eb891cc141fcd);
    const random_element_t MULTIPLIER2 = TO_UINT128(0xf9db042957460565, 0x77defab8be8f3a41);

    size_t i = 1, j = 0;

    for (size_t _ = 0; _ < MAX(RANDOM_STATE_SIZE, seed_array_length); _++) {
        random->state[i] = (random->state[i] ^ ((random->state[i - 1] ^ (random->state[i - 1] >> (RANDOM_BITS - 2))) * MULTIPLIER1)) + seed_array[j] + j;

        i += 1;
        j += 1;

        if (i >= RANDOM_STATE_SIZE) {
            random->state[0] = random->state[RANDOM_STATE_SIZE - 1];
            i = 1;
        }

        if (j >= seed_array_length) {
            j = 0;
        }
    }

    for (size_t _ = 0; _ < RANDOM_STATE_SIZE - 1; _++) {
        random->state[i] = (random->state[i] ^ ((random->state[i - 1] ^ (random->state[i - 1] >> (RANDOM_BITS - 2))) * MULTIPLIER2)) - i;

        i += 1;

        if (i >= RANDOM_STATE_SIZE) {
            random->state[0] = random->state[RANDOM_STATE_SIZE - 1];
            i = 1;
        }
    }

    random->state[0] = TO_UINT128(0x8000000000000000, 0x0000000000000000);
}

void random_init(random_t *random, uint8_t *seed_data, size_t seed_length) {
    const random_element_t SEED = TO_UINT128(0x506f91c5b392a98e, 0x2c5912ca0d55cedf);

    if (random->is_initialized) {
        return;
    }

    random_init_by_value(random, SEED);

    size_t seed_array_length = MAX(
        sizeof(random_element_t) * RANDOM_STATE_SIZE,
        seed_length + (sizeof(random_element_t) - seed_length % sizeof(random_element_t)) % sizeof(random_element_t)
    );

    uint8_t seed_array[seed_array_length];

    for (size_t i = 0; i < seed_array_length; i++) {
        if (i < seed_length) {
            seed_array[i] = seed_data[i];
        }
        else {
            seed_array[i] = 0;
        }
    }

    memfrob(seed_array, seed_array_length);
    random_init_by_array(random, (random_element_t *)&seed_array, seed_array_length / sizeof(random_element_t));

    random->index = RANDOM_STATE_SIZE;
    random->element_index = 0;

    random->is_initialized = true;
}

void random_clear(random_t *random) {
    if (!random->is_initialized) {
        return;
    }

    random->is_initialized = false;
}

void random_twist(random_t *random) {
    const random_element_t LOWER = TO_UINT128(0x0000000000000000, 0x7FFFFFFFFFFFFFFF);
    const random_element_t UPPER = TO_UINT128(0xFFFFFFFFFFFFFFFF, 0x8000000000000000);
    const random_element_t MAGNITUDE = TO_UINT128(0x928909a4362f201d, 0xa792e0cfc52135e3);

    for (size_t i = 0; i < RANDOM_STATE_SIZE / 2; i++) {
        random_element_t value = (random->state[i] & UPPER) | (random->state[i + 1] & LOWER);
        random->state[i] = random->state[i + RANDOM_STATE_SIZE / 2] ^ (value >> 1);

        if ((value & 1) == 1) {
            random->state[i] ^= MAGNITUDE;
        }
    }

    for (size_t i = RANDOM_STATE_SIZE / 2; i < RANDOM_STATE_SIZE - 1; i++) {
        random_element_t value = (random->state[i] & UPPER) | (random->state[i + 1] & LOWER);
        random->state[i] = random->state[i - RANDOM_STATE_SIZE / 2] ^ (value >> 1);

        if ((value & 1) == 1) {
            random->state[i] ^= MAGNITUDE;
        }
    }

    random_element_t value = (random->state[RANDOM_STATE_SIZE - 1] & UPPER) | (random->state[0] & LOWER);
    random->state[RANDOM_STATE_SIZE - 1] = random->state[RANDOM_STATE_SIZE / 2 - 1] ^ (value >> 1);

    if ((value & 1) == 1) {
        random->state[RANDOM_STATE_SIZE - 1] ^= MAGNITUDE;
    }
}

random_element_t random_temper(random_t *random, random_element_t value) {
    const random_element_t VAL1 = TO_UINT128(0x9742f68607cd2e15, 0xedbd04ed91775f02);
    const random_element_t VAL2 = TO_UINT128(0xaf42dca1a3cdf9be, 0xd8e4c2087837b878);
    const random_element_t VAL3 = TO_UINT128(0x152c95e4dec535d5, 0x893a7dd5f111f229);

    value ^= (value >> 92);
    value ^= (value << 111) & VAL1;
    value ^= (value >> 59) & VAL2;
    value ^= (value << 45) & VAL3;
    value ^= (value >> 34);

    return value;
}


random_element_t random_next(random_t *random, size_t bits) {
    if (!random->is_initialized) {
        return 0;
    }

    random_element_t result = 0;

    while (bits > 0) {
        if (random->index >= RANDOM_STATE_SIZE) {
            random_twist(random);
            random->index = 0;
        }

        result <<= bits;

        size_t left = RANDOM_BITS - random->element_index;
        size_t take = MIN(bits, left);

        size_t shift = RANDOM_BITS - random->element_index - take;

        random_element_t mask = ((random_element_t)1 << take) - 1;

        if (take == RANDOM_BITS) {
            mask = (random_element_t)-1;
        }

        random_element_t value = random_temper(random, random->state[random->index]);

        result |= (value >> shift) & mask;

        random->element_index += take;

        if (random->element_index >= RANDOM_BITS) {
            random->index += 1;
            random->element_index = 0;
        }

        bits -= take;
    }

    return result;
}
