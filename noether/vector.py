'''Noether: Useful numpy bindings'''

import math

import numpy as np

from .helpers import product, intify

def Vector(*x, dtype=None):
    if len(x) == 1:
        x = x[0]
    return np.array(list(x), dtype=dtype)

def Matrix(*x, shape=None, dtype=None):
    '''Return a matrix. Attempts to automatically shape to square.
    
    Try Matrix(1, 2, 3, 4)'''
    v = Vector(*x, dtype=dtype)
    n = len(v)
    
    unknowns = shape.count(...)
    if unknowns == 1:
        rem = len(x) // product(i for i in shape if i != ...)
        shape = tuple(rem if i == ... else i for i in shape)
        
    elif unknowns > 1:
        raise ValueError('More than one unknown in length')
    
    if shape:
        return v.reshape(shape)
    
    if len(v.shape) == 1:
        # not already shaped: attempt to match square matrix
        a = math.sqrt(n)
        b = int(a)
        if a == b:
            return v.reshape((b, b))
