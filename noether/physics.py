'''Default REPL namespace for Noether.'''

import math

from math import (
    log, exp, floor, ceil,
    radians as rad, degrees as deg
)

from .trigonometry import rad, deg, TrigonometryState as _trigState

from .helpers import clear, intify
from .constants import *

from . import units

import numpy as np

trig = _trigState(useRadians=True)
for name in 'sin cos tan asin acos atan atan2'.split():
    globals()[name] = getattr(trig, name)

del name

#% Calculus

def sqrt(x):
    return x ** 0.5

def differentiate(f, dx=0.0000001):
    def df(x):
        return (f(x+dx)-f(x))/dx
    return df

def sign(x):
    if x == 0:
        return 0
    elif x < 0:
        return -1
    else:
        return +1
