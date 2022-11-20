"""
Fundamental units and unit-defining helpers from which all other units derive.
"""

from typing import Dict, List, Tuple
from ...conf import conf

from ..dimension import Dimension
from ..measure import Measure
from ..unit import Unit

BASE_UNITS = (
    (-3, "luminosity",  "J", "cd",  True,  "candela"),
    (-2, "current",     "I", "A",   True,  "amp", "ampere"),
    (-1, "temperature", "Θ", "K",   True,  "kelvin"),
    ( 1, "mass",        "M", "kg",  False, "kilogram"),
    ( 2, "substance",   "N", "mol", True, "mole"),
    ( 3, "length",      "L", "m",   True, "metre", "meter"),
    ( 4, "time",        "T", "s",   True, "second")
)

_prefix = Tuple[str, str, float]
prefixes: Dict[str, Tuple[
    List[Unit], List[_prefix]]
]
prefixes = {
    "no_prefix": ([], (
        ("", "", 1),
    )),
    "SI_small": ([], (
        ("quecto", "y",  1e-30),
        ("ronto", "y",  1e-27),
        ("yocto", "y",  1e-24),
        ("zepto", "z",  1e-21),
        ("atto",  "a",  1e-18),
        ("femto", "f",  1e-15),
        ("pico",  "p",  1e-12),
        ("nano",  "n",  1e-9),
        ("micro", "µ",  1e-6),
        ("milli", "m",  1e-3),
    )),
    "SI_large": ([], (
        ("kilo",  "k",  1e3),
        ("mega",  "M",  1e6),
        ("giga",  "G",  1e9),
        ("tera",  "T",  1e12),
        ("peta",  "P",  1e15),
        ("exa",   "E",  1e18),
        ("zetta", "Z",  1e21),
        ("yotta", "Y",  1e24),
        ("ronna", "R",  1e27),
        ("quetta", "Q",  1e30),
    )),
    "SI_rest": ([], (
        # not used for scaling, but added to any SI units
        ("centi", "c",  1e-2),
        ("deci",  "d",  1e-1),
        ("deca",  "da", 1e1),
        ("hecto", "h",  1e2),
    )),
    "SI_fun": ([], (
        ("micri", "mc", 1e-14),
        ("dimi", "dm", 1e-4),
        ("hebdo", "H", 1e7),
        # still in our hearts
        # https://scitech.blogs.cnn.com/2010/03/04/hella-proposal-facebook/
        ("hella", "ha", 1e27),

        ("quecto", "q", 1e-30),
        ("ronto", "r", 1e-27),
        ("ronna", "R", 1e27),
        ("quecca", "Q", 1e30),

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

conf.register("prefix_fun", bool, False, """\
Enable historical or other nonstandard SI prefixes""")

conf.register("prefix_IEC", bool, True, """\
Enable binary data prefixes (eg mebibyte = 1024^2 byte)""")

units_SI = set()


def U(
        value, *symbols, display=None,
        si=False, si_large=False, iec=False
    ):
    unit = Unit(value, *symbols, is_display=display)

    prefixes["no_prefix"][0].append(unit)

    if si:
        units_SI.add(unit)
        si_large = True

        prefixes["SI_small"][0].append(unit)
        prefixes["SI_rest"][0].append(unit)
        if conf.prefix_fun:
            prefixes["SI_fun"][0].append(unit)

    if si_large:
        prefixes["SI_large"][0].append(unit)

    if iec and conf.prefix_IEC:
        prefixes["IEC"][0].append(unit)
    return unit

# SI units


for order, name, dim_sym, unit_sym, si, *units in BASE_UNITS:
    dim = Dimension.new(name, dim_sym, unit_sym, order=order*1000)
    globals()[name] = dim
    unit = U(dim, unit_sym, si=si)
    for name in units:
        globals()[name] = unit

del dim, unit

dimensionless = Dimension()
