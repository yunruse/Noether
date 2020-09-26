from .helpers import exp_mantissa, intify


def dict_invert(d): return dict(map(reversed, list(d.items())))


SUPERSCRIPT = str.maketrans(
    "-0123456789",
    "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"
)

NONBREAKING = {
    0x20: 0xA0,  # SPACE
    0x2009: 0x202F  # THIN SPACE
}


def superscript(number, unicode: bool = False):
    return str(number).translate(SUPERSCRIPT) if unicode else '^' + str(number)


def _scinot(number, dec, uni, lo, hi):
    exp, man = exp_mantissa(number)
    if lo is not None and hi is not None and lo < exp < hi:
        # avoid exponent for human-like values
        dec -= exp
        exp = None
        man = number

    num = ""
    if exp:
        num = "10" + superscript(exp, uni)
        if man == 1:
            return num
        elif man == -1:
            return "-" + num
        else:
            num = "×" + num

    return str(intify(round(man, dec))) + num


def number_string(
    number: float,
    plus_minus: float = 0,
    decimals: int = 2,
    as_unit: bool = False,
    unicode_exponent: bool = False,
    formatter=None,
    natural_leading_zeros: int = 2,
    natural_digits: int = 4,
):
    """Format a number with an uncertainty"""

    s_exp = ""
    if plus_minus:
        exp_num, _ = exp_mantissa(number)
        exp_pm, _ = exp_mantissa(plus_minus)
        exps_differ = abs(exp_num - exp_pm) > natural_digits
        def is_human(x): return -natural_leading_zeros < x < natural_digits
        sharing_unwieldy = exps_differ or is_human(
            exp_num) and is_human(exp_num)
        if not sharing_unwieldy:
            exp_shared = min(exp_num, exp_pm)
            number /= 10**exp_shared
            plus_minus /= 10**exp_shared
            s_exp = '×10' + superscript(exp_shared, unicode_exponent)

    s = ""
    if not callable(formatter):
        def formatter(x): return _scinot(
            x, decimals, unicode_exponent, -natural_leading_zeros, natural_digits)
    if number:
        s += formatter(number)
    if plus_minus:
        s += " ± " + formatter(plus_minus)
    s = s.strip() or "0"
    if s_exp or as_unit and number and plus_minus:
        s = "(" + s + ")" + s_exp
    return s
