"""Noether: Scaling of numbers (a×10^b)"""

from ..helpers import intify, exp_mantissa
from ..display import superscript

__all__ = "prefix prefixify".split()


class prefix:
    pass


#yapf: disable
prefix_SI = (
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
)
prefix_IEC = (
    ("kibi",  "Ki", 2**10),
    ("mebi",  "Mi", 2**20),
    ("gibi",  "Gi", 2**30),
    ("tebi",  "Ti", 2**40),
    ("pebi",  "Pi", 2**50),
    ("exbi",  "Ei", 2**60),
    ("zebi",  "Zi", 2**70),
    ("yobi",  "Yi", 2**80),
)

#yapf: enable

# TODO: this is hacky
for name, symbol, factor in prefix_SI + prefix_IEC:
    for i in (name, symbol):
        setattr(prefix, i, factor)

def prefixify(num):
    """Returns a number and any fitting SI prefix."""
    if not isinstance(num, (float, int)):
        return num, ""
    exp, mantissa = exp_mantissa(num, 10)
    for _, prefix, pExp in _prefixes.items():
        if -2 < exp - pExp < 3:
            return mantissa * 10**exp, prefix
    else:
        return num, ""
