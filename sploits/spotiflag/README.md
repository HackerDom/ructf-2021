# RuCTF 2021 | Spotiflag

## Description

The service allows us to generate a song from the given text description.

![generate](images/generate.png)

When we have entered some text and pressed `Generate` button, the website starts to play a WAV file:

![listen](images/listen.png)

If we open the WAV in Audacity, we will see a lot of tones with certain frequencies:

![tones](images/tones.png)

## Solution

While it was the web service, the main goal of the challenge is reversing the [spotiflag](../../services/spotiflag/spotiflag/spotiflag) binary, which was running as a separate service.

The source code of the binary ([internal/spotiflag/](../../internal/spotiflag/)) was not given to the participants.

TLDR:

1. Recognize [Mersenne twister](https://en.wikipedia.org/wiki/Mersenne_Twister) pseudorandom generator.
2. Find out how to reverse MT state and retrieve the initial seed array.
3. Find out how to extract MT output from WAV file frequencies array.

First look at the file [src/main.c](../../internal/spotiflag/src/main.c). At the entry point it just starts the forking UNIX-socket server and waits for connections. On each connection it reads `description` text and construct a WAV file from it. The WAV file is constructed from sequence of frequencies, each frequency is delivered as an output of some PRNG, and the PRNG itself is seeding by `description` data.

Then look at the file [src/random.c](../../internal/spotiflag/src/random.c). It contains typical functions for MT:

```c
void random_init_by_value(random_t *random, random_element_t seed_value);
void random_init_by_array(random_t *random, random_element_t *seed_array, size_t seed_array_length);
void random_twist(random_t *random);
random_element_t random_temper(random_t *random, random_element_t value);
random_element_t random_next(random_t *random, size_t bits);
```

First the `description` parameter is passing to `random_init_by_array()` function and used as initial seed of random generator. After the seeding we have got the internal `state` array of 32 elements, each of them has 128 bits. Also, there is `index` variable pointing to current `state` element, initially it points to the last element.

`random_next()` function generates the integer of `bits` length. It uses `random_twist()` and `random_temper()` to shuffle `state` array and modify the output.

Each frequency of WAV file contains 10 bits of consecutive output of the generator. So, if one could extract sufficiently many frequencies from the WAV file, then he can construct the original `state`, reverse the `random_init_by_array()` transformation and get the original `description`.

Example algorithm for MT seed recovering is described in [mt.py](mt.py).

Participants don't really need to implement it by hand, because the used MT algorithm is similar to well-known existing implementations, such as [cpython's `_randommodule.c`](https://github.com/python/cpython/blob/main/Modules/_randommodule.c). So, there already are a lot of articles about attacking Mersenne twister in Internet. But, basically, there are only two different approaches:

- use [z3 solver](https://github.com/Z3Prover/z3) to define the same algorithm in symbolic expressions and solve the equations (slower)
- carefully write the inverse algorithm to each random function and use them in right order (faster)

The reference code in [mt.py](mt.py) is using the second approach.

## Fix

The important fact: one needs to know the entire `state` of MT to reverse the seed. If the attacker have got less than the full `state`, he can't efficiently recovert the seed. The `state` itself could be recovered from MT outputs, using the inverse function of `random_temper()`. So, the attacker needs to download the WAV file with flag.

When one starts downloading the WAV file from server, he doesn't get the entire file at once. Instead, the server splits the WAV file to the chunks of 64 KB each.

The entire WAV file contains about 12 chunks, but the checker **always** downloads only 8 chunks.

So, it's easy to fix the service: just limit the downloading WAV file by 8 chunks.

## Exploit

Example sploit: [sploit.py](sploit.py)
