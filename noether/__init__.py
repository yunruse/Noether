"""Noether: Physics calculator"""

__author__ = "Mia yun Ruse"
__copyright__ = "Copyright 2018 Mia yun Ruse"
__status__ = "Prototype"
__email__ = "s-noether@yunru.se"

# Extras here are used in namespace

import math
import cmath
import numpy as np

from .maths import (
    sin, cos, tan,
    asin, acos, atan
)

from math import (
    sinh, cosh, tanh,
    asinh, acosh, atanh,
    log, exp,
    floor, ceil
) # noqa: F401

from . import particles

from .helpers import *  # noqa: F401, F403
from .constants import *  # noqa: F401, F403

from .graphing import plot
from .matrix import Matrix, Vector  # noqa: F401

V = Vector