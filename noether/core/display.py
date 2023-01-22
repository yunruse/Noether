'''
Functions for transforming various numbers into strings.

Handles Unicode.
'''

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


class NoetherRepr:
    def __repr_code__(self):
        return str(self)

    def __noether__(self):
        return str(self)

    def __repr__(self):
        if conf.get('display_repr_code'):
            return self.__repr_code__()
        return self.__noether__()
