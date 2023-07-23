from typing import Iterable

from noether.display import DISPLAY_REPR_CODE, canonical_number, plus_minus_symbol
from ...config import conf
from ..Measure import Measure
from ..Unit import Unit


# TODO: should & be replaced with +?
# It would slightly make things confusing in fairness.
# Maybe a flag could handle it?

class LinearUnit(Unit):
    """
    A linear combination of units, like `foot & inch`.

    Useful for display purposes.
    """
    units: list[Unit]

    def __init__(self, units: Iterable[Unit]):
        units = sorted(units, reverse=True)
        object.__setattr__(self, 'units', units)
        Unit.__init__(self, units[0])

    def __and__(self, unit: 'Unit | LinearUnit'):
        if isinstance(unit, LinearUnit):
            return LinearUnit(self.units + unit.units)
        else:
            return LinearUnit(self.units + [unit])

    # |~~\ '      |
    # |   ||(~|~~\|/~~|\  /
    # |__/ |_)|__/|\__| \/
    #         |        _/

    def __repr__(self):
        if conf.get(DISPLAY_REPR_CODE):
            return self._repr_code()
        return self.__noether__()

    def _repr_code(self):
        return 'ChainedUnit({})'.format(', '.join(
            x.name for x in self.units
        ))

    def __noether__(self):
        if conf.get('info_dimension'):
            return f'{self}  # {self.dim.name()}'
        return str(self)

    def __rich__(self):
        if conf.get('info_dimension'):
            return f'{self}[green italic]  # {self.dim.name()}'
        return str(self)

    def __str__(self):
        return ' & '.join([x.name for x in self.units])

    def _repr_measure(self, measure: Measure):
        value = measure._value
        chunks = []
        for i, unit in enumerate(self.units):
            if i == len(self.units)-1:
                dv = value / unit._value
            else:
                dv, value = divmod(value, unit._value)
            if dv:
                chunks.append(f'{canonical_number(dv)} {unit.symbol}')

        result = ' + '.join(chunks)

        if measure.stddev is not None:
            for su in self.units:
                if measure.stddev > su._value:
                    break
            pm = plus_minus_symbol()
            dv = measure.stddev / su._value
            result += f' {pm} {canonical_number(dv)} {su.symbol}'

        return result
