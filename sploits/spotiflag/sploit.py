#!/usr/bin/env python3

import mt
import sys
import numpy as np
import scipy.fft as fft

from typing import List
from scipy.io import wavfile


BASE_FREQUENCY = 256
TONE_DISTANCE = 1
TONE_DURATION = 0.25
TONE_BITS = 10


def read_frequency(data: np.ndarray, sample_rate: int, prec: int) -> int:
    size = prec * len(data)

    fft_data = fft.fft(data, n=size)
    fft_freqs = fft.fftfreq(size, 1 / sample_rate)

    freq_index = np.argmax(np.abs(fft_data))

    return int(fft_freqs[freq_index])


def extract_freqs(channel: np.ndarray, sample_rate: int, prec: int) -> List[int]:
    tone_length = int(sample_rate * TONE_DURATION)
    tones_count = len(channel) // tone_length + 1
    freqs = []

    for i in range(tones_count):
        tone = channel[i * tone_length: (i + 1) * tone_length]
        freq = read_frequency(tone, sample_rate, prec)
        freqs.append(freq)

    return freqs


def extract_state(freqs: List[int]) -> List[int]:
    freqs = list(freqs)

    outputs = [(x - BASE_FREQUENCY) // TONE_DISTANCE for x in freqs]
    bits = ''.join(bin(x)[2:].zfill(TONE_BITS) for x in outputs)

    state = []

    for i in range(mt.STATE_SIZE):
        part = bits[i * mt.BITS:(i + 1) * mt.BITS]
        state.append(int(part, 2))

    return state


def main():
    prec = 16

    sample_rate, data = wavfile.read(sys.argv[1])
    all_freqs = []

    for i in range(data.ndim):
        channel = data[:, i]
        freqs = extract_freqs(channel, sample_rate, prec)

        if freqs[-1] == 0:
            freqs.pop()

        all_freqs.extend(freqs)

    state = extract_state(all_freqs)

    seed_array = mt.recover_seed(state)
    seed_data = mt.array_to_bytes(seed_array)

    print(seed_data)


if __name__ == '__main__':
    main()
