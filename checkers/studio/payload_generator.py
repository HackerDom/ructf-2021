#!/usr/bin/env python3
import os
import random 

FLAG_OFFSET = 2712
TARGET = './generated/'

def get(flag):
    error = ""
    for i in range(2):
        try:
            return __get(flag)
        except Exception as e:
            error = e
    raise OSError(str(error))


def __get(flag):
    res = bytearray()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    files = os.listdir(TARGET)
    payload_name = random.choice(files)

    with open(os.path.join(dir_path, TARGET + payload_name), 'rb') as f:
        _, offset = payload_name.split('_')
        offset = int(offset)
        content = bytearray(f.read())
        res.extend(content[:offset])
        enc_flag = flag.encode()
        res.extend(bytearray(enc_flag))
        res.extend(content[offset+32:])
    return res
