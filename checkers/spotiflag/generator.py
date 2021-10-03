#!/usr/bin/env python3

import random
import string


LETTERS_WEIGHTS = {
    'E': 1260,
    'T': 937,
    'A': 834,
    'O': 770,
    'N': 680,
    'I': 671,
    'H': 611,
    'S': 611,
    'R': 568,
    'L': 424,
    'D': 414,
    'U': 285,
    'C': 273,
    'M': 253,
    'W': 234,
    'Y': 204,
    'F': 203,
    'G': 192,
    'P': 166,
    'B': 154,
    'V': 106,
    'K': 87,
    'J': 23,
    'X': 20,
    'Q': 9,
    'Z': 6
}


WEIGHTS = [LETTERS_WEIGHTS[letter] / 100 for letter in string.ascii_uppercase]


def word_generate() -> str:
    word_length = random.randint(2, 7)

    return ''.join(random.choices(
        string.ascii_lowercase,
        weights=WEIGHTS,
        k=word_length
    ))


def random_text(min_length: int, max_length: int) -> str:
    required_length = random.randint(min_length, max_length)

    words = []
    length = 0
    punctuation = '.,!?'
    next_capitalize = False

    while length < required_length:
        word = word_generate()

        if random.randint(0, 5) == 0:
            word += random.choice(punctuation)
            next_capitalize = True

        if next_capitalize or random.randint(0, 15):
            word = word.capitalize()
            next_capitalize = False

        words.append(word)
        length += len(word) + 1

    words.append(word_generate() + '.')

    return ' '.join(words)
