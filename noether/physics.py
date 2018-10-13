'''Namespace containing functions loaded into Noether by default.'''

import functools
import math
import os

import units
from constants import *
from math import log, exp, floor, ceil, radians as rad, degrees as deg

class _asNamed:
    '''Nicety to allow statements to quickly do functions.'''
    __slots__ = 'f'
    def __init__(s, f):
        s.f = f
    
    def __repr__(s):
        return s.f()

@_asNamed
def clear():
    return '\n' * 200

#% Trigonometry


useRadians = True

@_asNamed
def radians():
    global useRadians
    useRadians = True
    return 'Okay, set trigonometric mode to radians.'

@_asNamed
def degrees():
    global useRadians
    useRadians = False
    return 'Okay, set trigonometric mode to degrees.'

sin = functools.wraps(math.sin)(lambda x: math.sin(x if useRadians else rad(x)))
cos = functools.wraps(math.cos)(lambda x: math.cos(x if useRadians else rad(x)))
tan = functools.wraps(math.tan)(lambda x: math.tan(x if useRadians else rad(x)))

asin = functools.wraps(math.asin)(lambda x: math.asin(x) if useRadians else deg(math.asin(x)))
acos = functools.wraps(math.acos)(lambda x: math.acos(x) if useRadians else deg(math.acos(x)))
atan = functools.wraps(math.atan)(lambda x: math.atan(x) if useRadians else deg(math.atan(x)))
atan2 = functools.wraps(math.atan2)(
    lambda y, x: math.atan2(y, x) if useRadians else deg(math.atan2(y, x)))


#% Calculus


def differentiate(f, dx=0.0000001):
    def df(x):
        return (f(x+dx)-f(x))/dx
    return df

#% Graphing

_graphingActive = False

@_asNamed
def doGraphing():
    global _graphingActive, np, matplotlib, plt
    
    if _graphingActive:
        return 'Already started up graphing.'
    _graphingActive = True
    import numpy as np
    import matplotlib
    from matplotlib import pyplot as plt
    return 'Started graphing (np, matplotlib, plt).'

matplotlib = doGraphing
np = doGraphing
plt = doGraphing

def plot(*funcs, startx=-6, endx=6, axis='x', n=2000, starty=None, endy=None):
    repr(doGraphing)
    
    fig, axes = plt.subplots()
    if starty and endy:
        axes.set_ylim(starty, endy)

    x = np.linspace(startx, endx, n)
    axes.plot([startx, endx], [0, 0], 'gray', lw=0.5)

    ys = [(f, np.vectorize(f)(x)) for f in funcs]
    starty = starty or min(min(y) for f, y in ys)
    endy = endy or max(max(y) for f, y in ys)
    
    axes.plot([0, 0], [starty, endy], 'gray', lw=0.5)
    
    for f, y in ys:
        if axis == 'x':
            axes.plot(x, y, label=f.__name__)
        else:
            axes.plot(y, x, label=f.__name__)
            
    if len(funcs) > 1:
        plt.legend()
    plt.show()
