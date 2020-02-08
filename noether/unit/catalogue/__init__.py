"""
noether.unit.catalogue: Catalogue of constants, units and dimensions

This module intends to catalogue every unit, dimension and physical constant
that should ever be useful in calculation.

It is explicitly coded in Python, as opposed to a config file,
so as to be as legible in how it expresses relations to other units.
The submodule is defined in sectioned files for convenience.
"""

from .. import Dimension, Measure, Unit

from .constants import *
from .fundamental import *
from .dimensions import *
from .si import *
from .conventional import *
from .cgs import *
from .imperial import *
from .historical import *
from .scientific import *
from .data import *
from .unusual import *
from .systems import *

# Name transmogrification

__all__ = []

units = dict(globals()).items()

for name, unit in units:
    displayName = name.replace("_", " ")
    if isinstance(unit, Dimension):
        unit.addName(name)
    elif isinstance(unit, Unit):
        unit.names += (displayName, )
    elif isinstance(unit, Measure):
        globals()[name] = unit = U(unit, name)
    else:
        continue

    __all__.append(name)

# Assign prefixes

for units, prefixes in (
    (prefixable_SI, prefix_SI),
    (prefixable_IEC, prefix_IEC)
):
    for unit in units:
        for pName, pSym, pFactor in prefixes:
            for names, prefix in ((unit.names, pName), (unit.symbols, pSym)):
                for name in names:
                    name = prefix + name.replace(" ", "_")
                    if name not in globals():
                        globals()[name] = Unit(unit * pFactor, name)
                        __all__.append(name)
