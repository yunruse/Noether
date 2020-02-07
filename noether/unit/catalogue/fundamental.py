"""
Fundamental units and unit defining helpers from which all other units derive.
"""

BASE_UNITS = (
    (1, "luminosity",  "J", "cd",  True,  "candela"),
    (2, "current",     "I", "A",   True,  "amp", "ampere"),
    (3, "temperature", "Θ", "K",   True,  "kelvin"),
    (4, "mass",        "M", "kg",  False, "kilogram"),
    (5, "substance",   "N", "mol", True, "mole"),
    (6, "length",      "L", "m",   True, "metre", "meter"),
    (7, "time",        "T", "s",   True, "second")
)


from ..dimension import Dimension
from ..measure import Measure
from ..unit import Unit
from ..scale import prefix_SI, prefix_IEC

prefixable_SI = set()
prefixable_IEC = set()

def U(value, *symbols, display=None, SI=False, IEC=False):
    unit = Unit(value, *symbols, is_display=display)
    if SI:
        prefixable_SI.add(unit)
    if IEC:
        prefixable_IEC.add(unit)
    return unit

# SI units

for display_order, name, dim_sym, unit_sym, SI, *units in BASE_UNITS:
    dim = Dimension.new(display_order, name, dim_sym, unit_sym)
    globals()[name] = dim
    unit = U(dim, unit_sym, SI=SI)
    for name in units:
        globals()[name] = unit

del dim, unit

dimensionless = Dimension()

distance = length
