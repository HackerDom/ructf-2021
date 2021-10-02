#!/usr/bin/env python3
import random
import os

def get():
    error = ""
    for i in range(2):
        try:
            return __get()
        except Exception as e:
            error = e
    raise OSError(str(error))


def __get():
    res = bytearray()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open('useragents') as fin:
        user_agents = [line.strip() for line in fin]
    return random.choice(user_agents)
