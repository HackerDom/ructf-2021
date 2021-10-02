#!/usr/bin/env python3


def get():
    error = ""
    for i in range(2):
        try:
            return __get()
        except Exception as e:
            error = e
    raise OSError(str(error))


def __get(flag):
    res = bytearray()
    with open('checker_payload', 'rb') as f:
        content = bytearray(f.read())
        res.extend(content[:2712])
        enc_flag =  flag.encode()
        res.extend(bytearray(enc_flag))
        res.extend(content[2712+32:])
    return res
