"""Noether: Scaling of numbers (a×10^b)"""

from ..helpers import intify
from .display import translate_by_if, SUPERSCRIPT

from math import log, floor

__all__ = "prefix exp_mantissa prefixify scinot number_string".split()


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

FLOATING_POINT_ERROR_ON_LOG_TENXPONENTS = 12

def exp_mantissa(num, base=10):
    """Returns e, m such that x = mb^e"""
    if num == 0:
        return 1, 0
    # avoid floating point error eg log(1e3, 10) = 2.99...
    exp = log(abs(num), base)
    exp = round(exp, FLOATING_POINT_ERROR_ON_LOG_TENXPONENTS)
    exp = floor(exp) # 1 <= mantissa < 10
    mantissa = num / (base**exp)
    return exp, mantissa


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


def scinot(num, precision=4, unicode_exponents=True, lower=-2, upper=3):
    """Return number in scientific notation.

    If the exponent of 10 is in the range of `lower` and `upper`, will simply round."""

    exp, man = exp_mantissa(num)

    # try avoiding exponent for small exponents if provided
    if lower is not None and upper is not None:
        if lower < exp < upper:
            precision -= exp
            exp = None
            man = num

    man = intify(man)

    if exp and man == 1:
        num = ""
    elif exp and man == -1:
        num = "-"
    else:
        num = str(intify(round(man, precision)))

    if exp:
        # special case of 10^n, -10^n
        if abs(man) != 1:
            num += "×"
        num += '10'
        num += translate_by_if(exp, SUPERSCRIPT, unicode_exponents, prefix='^')
    return num


def number_string(
        number,
        delta=0,
        asUnit=False,
        precision=2,
        unicode_exponent=False,
        lower=-2,
        upper=4,
):
    """
    Format a number and uncertainty.

    Specify asUnit=True to ensure the result is valid in multiplication,
    and specify `lower` and `upper` for naturalisation limits.
    """
    eN, _ = exp_mantissa(number)
    eD, _ = exp_mantissa(delta)
    sharedExp = 0

    if delta:
        exponentsDiffer = abs(eN - eD) < 4
        humanN = lower < eN < upper
        humanD = lower < eD < upper

        if not (exponentsDiffer or humanN or humanD):
            sharedExp = max(eN, eD)

    if sharedExp:
        sharedFactor = 10**sharedExp
        number /= sharedFactor
        delta /= sharedFactor
        sExp = scinot(sharedFactor,
                      1,
                      unicode_exponent,
                      lower=None,
                      upper=None)
    else:
        sExp = ""

    sNum = ""
    if number:
        sNum += scinot(number, precision, unicode_exponent, lower, upper)
    if delta:
        sNum += " ± " + scinot(delta, precision, unicode_exponent, lower,
                               upper)

    sNum = sNum.strip() or "0"
    if sExp or (number and delta and asUnit):
        sNum = "(" + sNum + ")" + sExp

    return sNum
