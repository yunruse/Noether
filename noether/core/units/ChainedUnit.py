from typing import Iterable
from ...config import conf
from ..Measure import Measure
from ..Unit import Unit


class ChainedUnit(Unit):
    "Multiple units 'chained together', like feet & inches, for display."
    units: list[Unit]

    def __init__(self, units: Iterable[Unit]):
        units = sorted(units, reverse=True)
        object.__setattr__(self, 'units', units)
        Unit.__init__(self, units[0])

    def __and__(self, unit: 'Unit | ChainedUnit'):
        if isinstance(unit, ChainedUnit):
            return ChainedUnit(self.units + unit.units)
        else:
            return ChainedUnit(self.units + [unit])

    # |~~\ '      |
    # |   ||(~|~~\|/~~|\  /
    # |__/ |_)|__/|\__| \/
    #         |        _/

    def __repr__(self):
        if conf.get('display_repr_code'):
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
        # TODO: handle stddev!
        value = measure.value
        chunks = []
        for i, unit in enumerate(self.units):
            if i == len(self.units)-1:
                dv = value / unit.value
            else:
                dv, value = divmod(value, unit.value)
            if dv:
                chunks.append(f'{dv} {unit.symbol}')

        return ' + '.join(chunks)
