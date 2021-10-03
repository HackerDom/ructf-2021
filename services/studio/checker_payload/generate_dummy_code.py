#!/usr/bin/python3

import random
import string

OPERATIONS = ['*', '/', '+', '-', '>>', '<<']


def rand_op(a, b):
    op = random.choice(OPERATIONS)
    return f'{a} = {a} {op} {b};'

def rand_cond(iner):
    a = random.randint(0, 1000)
    return f'if (argc == {a}) {{{iner}}}'


def define_int():
    s = ''.join(random.choices(string.ascii_lowercase, k=10))
    n = random.randint(0, 1000)
    return f'int {s} = {n};', s

def generate_shit():
    code = ''
    for i in range(random.randint(5, 20)):
        f, name = define_int()
        code += f + '\n'
        ops = '\n'
        for j in range(random.randint(5, 20)):
            f = rand_op(name, random.randint(5, 20))
            ops += '\t' + f + '\n'
        code += rand_cond(ops) + '\n'
    return code

print(generate_shit())

