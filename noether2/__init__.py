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
__copyright__ = "Copyright (c) 2018-2022 Mia yun Ruse (yunru.se)"
__status__ = "Alpha 0.1.3"
__email__ = "mia@yunru.se"

from .conf import conf, conf_exists

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

from .unit import *  # noqa: F401, F403

display = Unit.display

if not conf_exists:
    conf.save()
    print("""\
Welcome to Noether! Just so you know, the config file
~/.config/noether/default.conf has been created.
Check config with noether.conf, make changes,
and then save with noether.conf.save().
Cheerio!
""")
del conf_exists