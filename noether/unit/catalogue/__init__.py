"""
noether.unit.catalogue: Catalogue of constants, units and dimensions

This module intends to catalogue every unit, dimension and physical constant
that should ever be useful in calculation.

Said units are categorised by file, then section `# #`,
and rarely with subsection `# # #`.

Units are provided in their original name, with a _ in place of a
space for variable names. They are named in English, with all
common spelling variants, with the exception of historical units.

Some conventional shorthands are provided; there does not yet
exist a common rule as to what is a "common rule".

Metric (but not necessarily SI) units defined in this catalogue
have also been given their prefixed equivalents. This naturally
does not automatically apply to custom-defined units.
"""

from ...conf import conf
from .. import Dimension, Measure, Unit

from .constants import *
from .fundamental import *
from .dimensions import *

from .si import *
from .data import *

from .conventional import *
from .scientific import *
from .planck import planck, planck_g, planck_lh


for i in 'cgs imperial historical unusual'.split():
    conf.register(
        f"unit_{i}", bool, True, f"Enable import of {i} in the namespace.",
        at_import=True)
    exec(f'if conf.unit_{i}: from .{i} import *')
del i

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

for units, ps in prefixes.values():
    for unit in units:
        for pName, pSym, pFactor in ps:
            for names, prefix in ((unit.names, pName), (unit.symbols, pSym)):
                for name in names:
                    name = prefix + name.replace(" ", "_")
                    if name not in globals():
                        globals()[name] = Unit(unit * pFactor, name)
                        __all__.append(name)
