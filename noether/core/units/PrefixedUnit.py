from ..Unit import Unit
from ..Prefix import Prefix


class PrefixedUnit(Unit):
    "A prefixed unit e.g. megawatt, centiliter."
    unit: Unit
    prefix: Prefix

    def __init__(self, prefix: Prefix, unit: Unit):

        object.__setattr__(self, 'unit', unit)
        object.__setattr__(self, 'prefix', prefix)

        Unit.__init__(
            self,
            unit * prefix.value,
            [f'{prefix.prefix}{n}' for n in unit.names],
            [f'{prefix.symbol}{s}' for s in unit.symbols],
        )
