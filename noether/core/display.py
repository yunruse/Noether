'''
Functions for transforming various numbers into strings.

Handles Unicode.
'''

from math import log10
from decimal import Decimal
from numbers import Real
from .config import Config, conf

Config.register("display_unicode_symbols", True, '''\
Use Unicode symbols eg ± instead of +-.
''')

Config.register("display_unicode_exponent", True, '''\
Use Unicode superscripts eg xⁿ instead of x**n.
''')

Config.register("display_repr_code", False, '''\
Return code-like repr() instead of a more calculator-like representation.
''')


def plus_minus_symbol() -> str:
    if conf.get('display_unicode_symbols'):
        return '±'
    return '+-'


SUPERSCRIPT = str.maketrans(
    "0123456789-+=/()",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁼ᐟ⁽⁾"
)


def superscript(number):
    if conf.get('display_unicode_exponent'):
        return str(number).translate(SUPERSCRIPT)
    return f'**{number}'


def _to_decimal(number: Real):
    if isinstance(number, float):
        return Decimal(str(number))
    return Decimal(number)


def uncertainty(number: Decimal, stddev: Decimal):
    '''Display'''
    a = _to_decimal(number)
    b = _to_decimal(stddev)

    if not (0 < b < 1):
        return f'{a}({b})'

    ai, af = str(a).split('.', 1)
    bi, bf = str(b).split('.', 1)
    assert bi == '0'

    ad = len(af)
    bd = len(bf)
    az = bd - ad
    bz = -1 - b.adjusted()
    bf = bf[bz:]
    af += '0'*az

    return f'{ai}.{af}({bf})'


def canonical_number(number, stddev):
    if stddev is not None:
        if conf.get('measure_uncertainty_shorthand'):
            return uncertainty(number, stddev)
        else:
            pm = plus_minus_symbol()
            return f'{number} {pm} {stddev}'
    if isinstance(number, float) and number.is_integer():
        return repr(int(number))
    return repr(number)


class NoetherRepr:
    def repr_code(self):
        return str(self)

    def __noether__(self):
        return str(self)

    def __repr__(self):
        if conf.get('display_repr_code'):
            return self.repr_code()
        return self.__noether__()
