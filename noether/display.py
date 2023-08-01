'''
Functions for transforming various numbers into strings.

Handles Unicode.
'''

from decimal import Decimal
from fractions import Fraction
from math import ceil, log10
from noether.helpers import Real, removeprefix, removesuffix

from .config import Config, conf

DISPLAY_UNICODE_SYMBOLS = Config.register("display_unicode_symbols", True, '''\
Use Unicode symbols eg ± instead of +-.
''')

DISPLAY_UNICODE_EXPONENT = Config.register("display_unicode_exponent", True, '''\
Use Unicode superscripts eg xⁿ instead of x**n.
''')

DISPLAY_REPR_CODE = Config.register("display_repr_code", False, '''\
Return code-like repr() instead of a more calculator-like representation.
''')

DISPLAY_DIGITS = Config.register("display_digits", 9, '''\
If a number is more than this many digits, display in scientific notation.
Also, round to this many digits.
''')

# TODO: lakh
DISPLAY_UNDERSCORE_AFTER = Config.register("display_underscore_after", 5, '''\
If a whole number is more than this many digits, display thousands separators (underscores).
Set to -1 to disable.
''')


def plus_minus_symbol() -> str:
    if conf.get(DISPLAY_UNICODE_SYMBOLS):
        return '±'
    return '+-'


SUPERSCRIPT = str.maketrans(
    "0123456789-+=/()",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁼ᐟ⁽⁾"
)


def superscript(number):
    if conf.get(DISPLAY_UNICODE_EXPONENT):
        return str(number).translate(SUPERSCRIPT)
    return f'**{number}'


def _to_decimal(number: Real | str):
    if isinstance(number, Fraction):
        number = float(number)
    if isinstance(number, float):
        number = str(number)
    return Decimal(number)


def uncertainty(number: Real | str, stddev: Real | str):
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


def scinot(number: Real, digits: int | None = None):
    notation = format(number, f'.{digits}e' if digits is not None else 'e')
    num, exp = notation.split('e')

    while num.endswith('0'):
        num = num[:-1]
    num = removesuffix(num, '.')

    sign = '' if exp.startswith('+') else '-'
    exp = int(exp[1:])
    return f'{num}e{sign}{exp}'


def _fmt(number: Real):
    if number == 0:
        return '0'
    mag = log10(abs(number))
    DIGITS: int = conf.get(DISPLAY_DIGITS)
    n = str(round(number, DIGITS - ceil(mag)))
    if 'e' in n or (len(n) > DIGITS and not -3 < mag < 4):
        return scinot(number)

    m = ''
    if '.' in n:
        n, m = n.split('.')
        m = '' if m == '0' else '.'+m
    UNDERSCORE_DIGITS = conf.get(DISPLAY_UNDERSCORE_AFTER)
    if UNDERSCORE_DIGITS != -1 and len(n) > UNDERSCORE_DIGITS:
        n_ = ''
        for i, d in enumerate(reversed(n)):
            n_ += d
            if i % 3 == 2:
                n_ += '_'
        n = ''.join(reversed(n_))
        n = removeprefix(n, '_')

    return f'{n}{m}'


def canonical_number(number: Real, stddev: Real | None = None, display_shorthand: bool = False):
    if stddev is not None:
        if display_shorthand:
            return uncertainty(number, stddev)
        else:
            pm = plus_minus_symbol()
            return f'{_fmt(number)} {pm} {_fmt(stddev)}'
    if isinstance(number, float) and number.is_integer():
        return _fmt(int(number))
    return _fmt(number)
