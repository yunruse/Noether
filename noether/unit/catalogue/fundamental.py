"""
Fundamental units and unit defining helpers from which all other units derive.
"""

from ..measure import Unit, Measure, Dimension
from ..scale import prefix_SI, prefix_IEC

prefixable_SI = set()
prefixable_IEC = set()

def U(value, *symbols, display=None, SI=False, IEC=False):
    display = SI if display is None else display
    unit = Unit(value, *symbols, isDisplay=display)
    if SI:
        prefixable_SI.add(unit)
    if IEC:
        prefixable_IEC.add(unit)
    return unit

# SI units

def base_units():
    # yapf: disable
    _BASE_UNITS = (
        (1, "luminosity", "cd", True, "candela"),
        (2, "current", "A", True, "amp", "ampere"),
        (3, "temperature", "K", True, "kelvin"),
        (4, "mass", "kg", False, "kilogram"),
        (5, "substance", "mol", True, "mole"),
        (6, "length", "m", True, "metre", "meter"),
        (7, "time", "s", True, "second")
    )
    # yapf: enable

    for u in _BASE_UNITS:
        display_order, name, symbol, SI, *units = u
        dim = Dimension.new(display_order, name, symbol)
        globals()[name] = dim
        unit = U(dim, symbol, SI=SI)
        for name in units:
            globals()[name] = unit

base_units()

dimensionless = Dimension()

distance = length