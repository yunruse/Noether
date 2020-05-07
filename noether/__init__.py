"""
Noether: Physics calculator.

Noether attempts to function as the go-to scientific calculator for Python.
It holds almost every unit and constant defined by SI and CODATA, with a
rich dimensional system allowing for physical computation to be
easily verifiable.

The author endeavours to cite every data, but cannot claim responsibility
for the correctness of every field of science. Please report an issue if
a paper is incorrectly interpreted, outdated, or not cited.

Indeed, please inform the author of any constants, units, and dimensions
not present, no matter how petty.
"""

__author__ = "Mia yun Ruse"
__copyright__ = "Copyright 2018-2020 Mia yun Ruse"
__status__ = "Alpha 2"
__email__ = "s-noether@yunru.se"

from .conf import conf, conf_new

import math
import cmath

from math import (
    sinh, cosh, tanh,
    asinh, acosh, atanh,
    log, exp,
    floor, ceil
) # noqa: F401

from .unit import *  # noqa: F401, F403
from .unit import catalogue
from .unit.catalogue import *

from .particles import *

from . import (
    particles,
)

from .unit import *  # noqa: F401, F403

display = Unit.display

if conf_new:
    conf.save("default")
    print("""\
It appears that you are using Noether for the first time.
The file .config/noether/default.conf (in your user folder) has
been created, but you can toy with noe.conf and then use
noe.conf.save() to save your changes.
""")
del conf_new