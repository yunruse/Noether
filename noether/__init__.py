'''Noether: Physics calculator'''

__author__    = "Mia yun Ruse"
__copyright__ = "Copyright 2018 Mia yun Ruse"
__status__    = "Prototype"
__email__     = 's-noether@yunru.se'

from .helpers import *
from .constants import *
from .repl import repr_mod

#% Calculus

def differentiate(f, dx=0.0000001):
    def df(x):
        return (f(x+dx)-f(x))/dx
    return df
