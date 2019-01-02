"""Noether: Mathematical functions and niceties.

Implements standard functions in raw mathematical form, so
that may operate on dimensionless Units with uncertainties correctly."""

from functools import wraps

import numpy as np

from .unit import Unit
from .taylor import Sine, Cosine

pi = np.pi
tau = pi * 2


def differentiate(f, dx=0.0000001):
    @wraps(f)
    def df(x):
        return (f(x + dx) - f(x)) / dx
    df.__name__ += "-d"
    return df

raw_sin = Sine.compileTerms(6)
raw_cos = Cosine.compileTerms(6)


def sin(x):
    if not isinstance(x, Unit):
        return np.sin(x)
    elif x % pi == 0:
        return 0
    elif x < -pi or x > pi:
        return sin(((x + pi) % tau) - pi)
    elif x < 0:
        return -sin(-x)
    elif x < 1e-8:
        return x
    elif x > pi / 2:
        return sin(pi - x)
    elif x > pi / 4:
        return raw_cos(pi / 2 - x)
    else:
        return raw_sin(x)


def cos(x):
    if not isinstance(x, Unit):
        return np.cos(x)
    else:
        return sin(x - pi / 2)