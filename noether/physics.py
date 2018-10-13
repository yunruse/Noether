'''Default REPL namespace for Noether.'''

import math

from math import log, exp, floor, ceil, radians as rad, degrees as deg

from .trigonometry import rad, deg, TrigonometryState as _trigState

from .helpers import clear
from .constants import *

import units

import numpy as np

trig = _trigState(useRadians=True)
for name in 'sin cos tan asin acos atan atan2'.split():
    globals()[name] = getattr(trig, name)

#% Calculus

def differentiate(f, dx=0.0000001):
    def df(x):
        return (f(x+dx)-f(x))/dx
    return df
