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
__status__ = "Alpha 0.1.3"
__email__ = "s-noether@yunru.se"

from .conf import conf, conf_new

import math
import cmath

from math import (
    sinh, cosh, tanh,
    asinh, acosh, atanh,
    log, exp,
    floor, ceil
)

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
    conf.save()
    print("""\
Welcome to Noether! Just so you know, the config file
~/.config/noether/default.conf has been created. You can toy
about with noe.conf and then use noe.conf.save(), though.
""")
del conf_new
