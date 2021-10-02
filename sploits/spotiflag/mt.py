#!/usr/bin/env python3

from typing import List


# parameters
BITS = 128
STATE_SIZE = 32
SEED = 0x506f91c5b392a98e2c5912ca0d55cedf

# init by value
MULTIPLIER = 0x47f764020313fb982e74d56c083cfbbb

# init by array
MULTIPLIER1 = 0x9236e30df91d984e7c3eb891cc141fcd
MULTIPLIER2 = 0xf9db04295746056577defab8be8f3a41

# temper
VAL1 = 0x9742f68607cd2e15edbd04ed91775f02
VAL2 = 0xaf42dca1a3cdf9bed8e4c2087837b878
VAL3 = 0x152c95e4dec535d5893a7dd5f111f229

# twist
LOWER = 0x00000000000000007FFFFFFFFFFFFFFF
UPPER = 0xFFFFFFFFFFFFFFFF8000000000000000
MAGNITUDE = 0x928909a4362f201da792e0cfc52135e3


def memfrob(data: bytes) -> bytes:
    value = 1

    data = bytearray(data)

    for i in range(len(data)):
        data[-(i + 1)] ^= value
        value = (value * 11) % 251

    return bytes(data)


def init_by_value(value: int) -> List[int]:
    state = [value]

    for i in range(1, STATE_SIZE):
        value = (MULTIPLIER * (state[i - 1] ^ (state[i - 1] >> (BITS - 2)))) & ((1 << BITS) - 1)
        state.append(value + i)

    return state


def untemper_right(x: int, value: int, mask: int=(1 << BITS) - 1) -> int:
    all_bits = (1 << BITS) - 1

    for i in range(value, BITS + value, value):
        bits = ((1 << value) - 1) << max(BITS - i, 0)

        if i > BITS:
            bits >>= value - (BITS % value)

        y = (x ^ ((x >> value) & mask)) & bits
        x = y | (x & (all_bits ^ bits))

    return x


def untemper_left(x: int, value: int, mask: int=(1 << BITS) - 1) -> int:
    all_bits = (1 << BITS) - 1

    for i in range(value, BITS, value):
        bits = ((1 << value) - 1) << min(BITS - value, i)

        if i + value > BITS:
            bits = (bits << (value - (BITS % value))) & all_bits

        y = (x ^ ((x << value) & mask)) & bits
        x = y | (x & (all_bits ^ bits))

    return x


def untemper(x: int) -> int:
    x = untemper_right(x, 34)
    x = untemper_left(x, 45, VAL3)
    x = untemper_right(x, 59, VAL2)
    x = untemper_left(x, 111, VAL1)
    x = untemper_right(x, 92)

    return x


def untwist(twisted_state: List[int]) -> List[int]:
    untwisted_state = list(twisted_state)

    for i in reversed(range(STATE_SIZE // 2, STATE_SIZE)):
        value = twisted_state[i] ^ twisted_state[(i + STATE_SIZE // 2) % STATE_SIZE]

        if value & (1 << (BITS - 1)) != 0:
            value ^= MAGNITUDE

        untwisted_state[i] = (value << 1) & UPPER

    for i in reversed(range(STATE_SIZE // 2, STATE_SIZE)):
        result = 0
        value = twisted_state[i] ^ twisted_state[(i + STATE_SIZE // 2) % STATE_SIZE]

        if value & (1 << (BITS - 1)) != 0:
            value ^= MAGNITUDE
            result |= 1

        result |= (value << 1) & LOWER

        untwisted_state[(i + 1) % STATE_SIZE] = (untwisted_state[(i + 1) % STATE_SIZE] & UPPER) | result

    for i in reversed(range(STATE_SIZE // 2)):
        value = untwisted_state[i] ^ untwisted_state[(i + STATE_SIZE // 2) % STATE_SIZE]

        if value & (1 << (BITS - 1)) != 0:
            value ^= MAGNITUDE

        untwisted_state[i] = (value << 1) & UPPER

    for i in reversed(range(STATE_SIZE // 2)):
        result = 0
        value = twisted_state[i] ^ untwisted_state[(i + STATE_SIZE // 2) % STATE_SIZE]

        if value & (1 << (BITS - 1)) != 0:
            value ^= MAGNITUDE
            result |= 1

        result |= (value << 1) & LOWER

        untwisted_state[(i + 1) % STATE_SIZE] = (untwisted_state[(i + 1) % STATE_SIZE] & UPPER) | result

    return untwisted_state


def get_seed_array(state: List[int], initial_state: List[int], hint: int) -> List[int]:
    MOD = ((1 << BITS) - 1)

    # step 1
    state = list(state)
    state[0] = state[-1]

    expected_state = [None] * STATE_SIZE

    for i in reversed(range(1, 2)):
        value = ((state[i - 1] ^ (state[i - 1] >> (BITS - 2))) * MULTIPLIER2) & MOD
        state[i] = (state[i] + i) ^ value

    for i in reversed(range(2, STATE_SIZE)):
        value = ((state[i - 1] ^ (state[i - 1] >> (BITS - 2))) * MULTIPLIER2) & MOD
        expected_state[i] = (state[i] + i) ^ value

    expected_state[0] = expected_state[-1]
    expected_state[1] = state[1]

    # step 2
    seed_array = []
    intermediate_state = list(initial_state)

    value = ((expected_state[0] ^ (expected_state[0] >> (BITS - 2))) * MULTIPLIER1) & MOD
    expected_state[1] = ((expected_state[1] - (STATE_SIZE - 1) - hint) ^ value) & MOD

    expected_state[0] = initial_state[0]

    for i in range(1, STATE_SIZE):
        value = (intermediate_state[i - 1] ^ (intermediate_state[i - 1] >> (BITS - 2))) * MULTIPLIER1
        actual = ((intermediate_state[i] ^ value) + (i - 1)) & MOD
        seed_array.append((expected_state[i] - actual) & MOD)
        intermediate_state[i] = expected_state[i]

    return seed_array + [hint]


def array_to_bytes(array: List[int]) -> bytes:
    data = []

    for x in array:
        data.append(x.to_bytes(BITS // 8, 'little'))

    return b''.join(data)


def bytes_to_array(data: bytes) -> List[int]:
    array = []

    for i in range(0, len(data), BITS // 8):
        part = data[i:i+BITS // 8]
        array.append(int.from_bytes(part, 'little'))

    return array


def memfrob_array(array: List[int]) -> List[int]:
    data = array_to_bytes(array)
    data = memfrob(data)

    return bytes_to_array(data)


def recover_seed(outputs: List[int]) -> List[int]:
    hint = memfrob_array([0])[0]

    state = list(map(untemper, outputs))

    initial_state = init_by_value(SEED)
    untwisted_state = untwist(state)

    seed_array = get_seed_array(untwisted_state, initial_state, hint)

    return memfrob_array(seed_array)
