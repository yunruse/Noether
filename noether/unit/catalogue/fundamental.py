"""
Fundamental units and unit-defining helpers from which all other units derive.
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

prefixes = {
    # "tag": [units], (prefixes)
    "SI_small": ([], (
        ("yocto", "y",  1e-24),
        ("zepto", "z",  1e-21),
        ("atto",  "a",  1e-18),
        ("femto", "f",  1e-15),
        ("pico",  "p",  1e-12),
        ("nano",  "n",  1e-9),
        ("micro", "µ",  1e-6),
        ("milli", "m",  1e-3),
        ("centi", "c",  1e-2),
        ("deci",  "d",  1e-1),
    )),
    "SI_large": ([], (
        ("deca",  "da", 1e1),
        ("hecto", "h",  1e2),
        ("kilo",  "k",  1e3),
        ("mega",  "M",  1e6),
        ("giga",  "G",  1e9),
        ("tera",  "T",  1e12),
        ("peta",  "P",  1e15),
        ("exa",   "E",  1e18),
        ("zetta", "Z",  1e21),
        ("yotta", "Y",  1e24),
    )),
    "IEC": ([], (
        ("kibi",  "Ki", 2**10),
        ("mebi",  "Mi", 2**20),
        ("gibi",  "Gi", 2**30),
        ("tebi",  "Ti", 2**40),
        ("pebi",  "Pi", 2**50),
        ("exbi",  "Ei", 2**60),
        ("zebi",  "Zi", 2**70),
        ("yobi",  "Yi", 2**80),
    ))
}

from ..dimension import Dimension
from ..measure import Measure
from ..unit import Unit

units_SI = set()

def U(
        value, *symbols, display=None,
        SI=False, pSIs=False, pSIb=False, pIEC=False):
    unit = Unit(value, *symbols, is_display=display)
    if SI:
        units_SI.add(unit)
        pSIs = pSIb = True
    for b, tag in (pSIs, "SI_small"), (pSIb, "SI_large"), (pIEC, "IEC"):
        if b:
            prefixes[tag][0].append(unit)
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
