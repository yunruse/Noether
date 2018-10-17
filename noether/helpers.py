'''Noether: general standalone math and repl niceties'''

import math
import functools

__all__ = 'clear intify sqrt sign'.split()

class _asNamed:
    '''Nicety to allow statements to carry out functions'''
    __slots__ = 'f'
    def __init__(s, f):
        s.f = f
    
    def __repr__(s):
        return s.f()

@_asNamed
def clear():
    return '\n' * 200

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
