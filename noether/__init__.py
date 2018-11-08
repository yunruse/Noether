"""Noether: Physics calculator"""

__author__ = "Mia yun Ruse"
__copyright__ = "Copyright 2018 Mia yun Ruse"
__status__ = "Prototype"
__email__ = "s-noether@yunru.se"

from .helpers import *  # noqa: F401, F403
from .constants import *  # noqa: F401, F403
from .repl import repr_mod  # noqa: F401

from .matrix import Matrix, Vector  # noqa: F401

V = Vector


def differentiate(f, dx=0.0000001):
    def df(x):
        return (f(x + dx) - f(x)) / dx

    return df
