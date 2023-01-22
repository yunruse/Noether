'''
Prefixes a unit may take.
'''

from dataclasses import dataclass
from decimal import Decimal

from .config import Config, conf

Config.register("prefix_fun", False, """\
Enable historical or other nonstandard SI prefixes""")

Config.register("prefix_IEC", True, """\
Enable binary data prefixes (eg mebibyte = 1024^2 byte)""")


@dataclass
class Prefix:
    prefix: str
    symbol: str
    value: Decimal


class PrefixSet(list[Prefix]):
    __slots__ = ('name', )

    def __init__(
        self,
        name: str,
        prefixes: (None | list[Prefix] |
                   list[tuple[str, str, str | Decimal]]) = None
    ):
        self.name = name
        list.__init__(self)
        for prefix in prefixes or []:
            if not isinstance(prefix, Prefix):
                prefix, symbol, value = prefix
                prefix = Prefix(prefix, symbol, Decimal(value))
            self.append(prefix)

    def __repr__(self): return self.name


SI_small = PrefixSet('SI_small', [
    ("quecto", "y", '1e-30'),
    ("ronto", "y", '1e-27'),
    ("yocto", "y", '1e-24'),
    ("zepto", "z", '1e-21'),
    ("atto",  "a", '1e-18'),
    ("femto", "f", '1e-15'),
    ("pico",  "p", '1e-12'),
    ("nano",  "n", '1e-9'),
    ("micro", "µ", '1e-6'),
    ("milli", "m", '1e-3'),
])
SI_large = PrefixSet('SI_large', [
    ("kilo",  "k", '1e3'),
    ("mega",  "M", '1e6'),
    ("giga",  "G", '1e9'),
    ("tera",  "T", '1e12'),
    ("peta",  "P", '1e15'),
    ("exa",   "E", '1e18'),
    ("zetta", "Z", '1e21'),
    ("yotta", "Y", '1e24'),
    ("ronna", "R", '1e27'),
    ("quetta", "Q", '1e30'),
])
SI_conventional = PrefixSet('SI_conventional', [
    ("centi", "c", '1e-2'),
    ("deci",  "d", '1e-1'),
    ("deca",  "da", '1e1'),
    ("hecto", "h", '1e2'),
])
SI_fun = PrefixSet('SI_fun', [
    ("micri", "mc", '1e-14'),
    ("dimi", "dm", '1e-4'),
    ("hebdo", "H", '1e7'),
    # still in our hearts
    # https://scitech.blogs.cnn.com/2010/03/04/hella-proposal-facebook/
    ("hella", "ha", '1e27'),
])

_2 = Decimal('2')

IEC = PrefixSet('IEC', [
    ("kibi", "Ki", _2**10),
    ("mebi", "Mi", _2**20),
    ("gibi", "Gi", _2**30),
    ("tebi", "Ti", _2**40),
    ("pebi", "Pi", _2**50),
    ("exbi", "Ei", _2**60),
    ("zebi", "Zi", _2**70),
    ("yobi", "Yi", _2**80),
])

SI = SI_large + SI_small + SI_conventional
if conf.get('prefix_fun'):
    SI = SI + SI_fun
SI = PrefixSet('SI', SI)

if not conf.get('prefix_IEC'):
    IEC.clear()
