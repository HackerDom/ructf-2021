#!/usr/bin/env python3
import os

FLAG_OFFSET = 2712


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

    with open(os.path.join(dir_path, 'checker_payload'), 'rb') as f:
        content = bytearray(f.read())
        res.extend(content[:FLAG_OFFSET])
        enc_flag = flag.encode()
        res.extend(bytearray(enc_flag))
        res.extend(content[FLAG_OFFSET+32:])
    return res
