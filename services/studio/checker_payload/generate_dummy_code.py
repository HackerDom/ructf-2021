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

def generate_flag():
    flag_symbols = string.ascii_uppercase + string.digits
    return "".join((flag_symbols[random.randint(0, len(flag_symbols)-1)] for _ in range(31))) + "="

def define_flag():
    s = ''.join(random.choices(string.ascii_lowercase, k=10))
    val = generate_flag()
    return f'char * {s} = "{val}";', val

def define_string(l):
    s = ''.join(random.choices(string.ascii_lowercase, k=10))
    val = ''.join(random.choices(string.ascii_lowercase, k=l))
    return f'char * {s} = "{val}";', val

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

    strs_count = random.randint(5, 10)
    ops = []
    for i in range(strs_count):
        op, name = define_flag()
        ops.append(op)
    
    strs_count = random.randint(20, 100)
    ops = []
    for i in range(strs_count):
        op, name = define_string(random.randint(10, 100))
        ops.append(op)

    strs_count = random.randint(2, 5)
    ops = []
    for i in range(strs_count):
        op, name = define_string(random.randint(10000, 640000))
        ops.append(op)
    
    #flag_var_name = "".join(random.choices(string.ascii_lowercase, k=10))
    #ops[random.randint(0, strs_count)] = f'string {flag_var_name} = "{flag}";'

    code += '\n'.join(ops)

    return code


code = generate_shit()

print(code)
