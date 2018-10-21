'''Noether: general standalone math and repl niceties'''

import math
import os
import sys
import functools

__all__ = 'clear intify sqrt sign product tablify'.split()

def clear(isTerminal=True):
    if not isTerminal:
        print('\n' * 200)
    elif os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def bell():
    sys.stdout.write('\a')
    sys.stdout.flush()

def intify(x):
    '''Change to an int if it is equal to one.'''
    i = int(x)
    return i if x == i else x

@functools.wraps(math.sqrt)
def sqrt(x):
    # redefined to be nice of 
    return x ** 0.5

def sign(x):
    '''Return the mathematical sign of the particle.'''
    if isinstance(x, complex):
        return x / sqrt(x.imag**2 + x.real**2)
    if x == 0:
        return 0
    elif x < 0:
        return -1
    else:
        return +1

def product(iterable, start=1):
    for i in iterable:
        start *= i
    return start

def tablify(table, sep=' '):
    table = list(table)
    lens = [max(map(len, col)) for col in zip(*table)]
    return (sep.join(c + ' ' * (l-len(c))
             for c, l in zip(r, lens)) for r in table)
