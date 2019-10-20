"""
Noether: Physics calculator.

Noether attempts to function as the go-to scientific calculator for Python.
It holds almost every unit and constant defined by SI and CODATA, with a
rich dimensional system allowing for physical computation to be
easily verifiable.
"""

__author__ = "Mia yun Ruse"
__copyright__ = "Copyright 2018-2019 Mia yun Ruse"
__status__ = "Prototype"
__email__ = "s-noether@yunru.se"

import math
import cmath
import numpy as np


from math import (
    sinh, cosh, tanh,
    asinh, acosh, atanh,
    log, exp,
    floor, ceil
) # noqa: F401

from . import (
    particles,
    unit
)

from .unit import *  # noqa: F401, F403

from .graphing import plot
from .matrix import Matrix, Vector  # noqa: F401
