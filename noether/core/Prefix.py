'''
Prefixes a unit may take.
'''

from dataclasses import dataclass

from ..config import Config, conf

Config.register("PREFIX_fun", False, """\
Enable historical or other nonstandard SI prefixes""")

Config.register("PREFIX_iec", True, """\
Enable binary data prefixes (eg mebibyte = 1024^2 byte)""")


@dataclass(frozen=True)
class Prefix:
    prefix: str
    symbol: str
    value: float

    def __json__(self):
        return {
            'prefix': self.prefix,
            'symbol': self.symbol,
            'value': self.value
        }


class PrefixSet(list[Prefix]):
    __slots__ = ('name', )

    def __init__(
        self,
        name: str,
        prefixes: list[Prefix] | None = None
    ):
        self.name = name
        list.__init__(self, prefixes or [])

    @classmethod
    def from_list(
        cls,
        name: str,
        prefixes: list[tuple[str, str, float]]
    ):
        return cls(name, [Prefix(p, s, v) for p, s, v in prefixes])

    def __add__(self, other: 'PrefixSet'):
        return PrefixSet(
            f'{self.name} + {other.name}',
            list(self) + list(other))

    def __repr__(self):
        return self.name

    def __json__(self):
        return {'name': self.name, 'prefixes': [p.__json__() for p in self]}


SI_small = PrefixSet.from_list('SI_small', [
    ("milli", "m", 1e-3),
    ("micro", "µ", 1e-6),  # GCWM 11
    ("nano",  "n", 1e-9),  # GCWM 11
    ("pico",  "p", 1e-12),  # GCWM 11
    ("femto", "f", 1e-15),  # GCWM 12
    ("atto",  "a", 1e-18),  # GCWM 12
    ("zepto", "z", 1e-21),  # GCWM 19
    ("yocto", "y", 1e-24),  # GCWM 19
    ("ronto", "y", 1e-27),  # GCWM 26
    ("quecto", "y", 1e-30),  # GCWM 26
])
SI_large = PrefixSet.from_list('SI_large', [
    ("kilo",  "k", 1e3),
    ("mega",  "M", 1e6),  # GCWM 11
    ("giga",  "G", 1e9),  # GCWM 11
    ("tera",  "T", 1e12),  # GCWM 11
    ("peta",  "P", 1e15),  # GCWM 15
    ("exa",   "E", 1e18),  # GCWM 15
    ("zetta", "Z", 1e21),  # GCWM 19
    ("yotta", "Y", 1e24),  # GCWM 19
    ("ronna", "R", 1e27),  # GCWM 26
    ("quetta", "Q", 1e30),  # GCWM 26
])
SI_conventional = PrefixSet.from_list('SI_conventional', [
    ("centi", "c", 1e-2),
    ("deci",  "d", 1e-1),
    ("deca",  "da", 1e1),
    ("hecto", "h", 1e2),
])
SI_fun = PrefixSet.from_list('SI_fun', [
    ("micri", "mc", 1e-14),
    ("dimi", "dm", 1e-4),
    ("hebdo", "H", 1e7),
    # still in our hearts
    # https://scitech.blogs.cnn.com/2010/03/04/hella-proposal-facebook/
    ("hella", "ha", 1e27),
])

IEC = PrefixSet.from_list('IEC', [
    ("kibi", "Ki", 2**10),
    ("mebi", "Mi", 2**20),
    ("gibi", "Gi", 2**30),
    ("tebi", "Ti", 2**40),
    ("pebi", "Pi", 2**50),
    ("exbi", "Ei", 2**60),
    ("zebi", "Zi", 2**70),
    ("yobi", "Yi", 2**80),
    # ("robi", "Ri", 2**90),
    # ("quebi", "Qi", 2**100),
])

SI_all = SI_large + SI_small + SI_conventional
if conf.get('PREFIX_fun'):
    SI_all = SI_all + SI_fun

if not conf.get('PREFIX_iec'):
    IEC.clear()
