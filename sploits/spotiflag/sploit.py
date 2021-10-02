#!/usr/bin/env python3

import io
import sys
import requests
import numpy as np
import scipy.fft as fft

from typing import List
from scipy.io import wavfile

import mt


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


def extract_data(wav: bytes) -> bytes:
    prec = 16

    sample_rate, data = wavfile.read(io.BytesIO(wav))
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

    return seed_data


def download_wav(url: str, chunks_count: int) -> bytes:
    offset = 0
    chunks = []

    for i in range(chunks_count):
        headers = {
            'Range': f'bytes={offset}-'
        }

        chunk = requests.get(url, headers=headers).content

        chunks.append(chunk)
        offset += len(chunk)

    return b''.join(chunks)


def main():
    IP = sys.argv[1]
    PORT = 17171

    url = f'http://{IP}:{PORT}'

    for id in requests.get(f'{url}/api/list/').json():
        wav_url = f'{url}/api/listen/{id}/'
        wav = download_wav(wav_url, 16)

        flag = extract_data(wav)
        print(flag)


if __name__ == '__main__':
    main()
