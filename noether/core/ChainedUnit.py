from .Measure import Measure
from .Unit import Unit


class ChainedUnit(Unit):
    units: list[Unit]

    def __init__(self, unit: Unit, *units: tuple[Unit]):
        object.__setattr__(self, 'units',
                           sorted(set((unit, ) + units), reverse=True))
        Unit.__init__(self, unit)

    def __and__(self, unit: 'Unit | ChainedUnit'):
        if isinstance(unit, ChainedUnit):
            return ChainedUnit(*self.units, *unit.units)
        else:
            return ChainedUnit(*self.units, unit)

    def __repr__(self):
        return '{} ({})'.format(
            ' & '.join([x.name for x in self.units]),
            self.dim.canonical_name()
        )

    def __rich__(self):
        return '[bold]{}[/] ([italic]{})'.format(
            '[/] & [bold]'.join([x.name for x in self.units]),
            self.dim.canonical_name()
        )

    def _display_measure(self, measure: Measure):
        # TODO: handle stddev!
        value = measure.value
        chunks = []
        for i, unit in enumerate(self.units):
            if i == len(self.units)-1:
                dv = value / unit.value
            else:
                dv, value = divmod(value, unit.value)
            chunks.append(f'{dv} {unit.symbol}')

        return ' + '.join(chunks)
