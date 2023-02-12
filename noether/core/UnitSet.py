'''
List of units used for display purposes.

Also handles dimension names.
'''

from typing import TypeVar
from .Dimension import Dimension
from .Unit import Unit

T = TypeVar('T', Unit, Dimension, 'UnitSet')


class UnitSet(set[Unit]):
    units: dict[Dimension, list[Unit]]
    dimension_names: dict[Dimension, list[str]]

    dimension_symbol: dict[str, str]

    def __init__(self, *items: Unit):
        super().__init__()

        self.units = dict()
        self.dimension_names = dict()
        self.dimension_symbol = dict(dimensionless='')
        self.register(*items)

    def add(self, value: T, *names: str) -> T:
        if isinstance(value, Dimension):
            self.dimension_names.setdefault(value, [])
            for n in names:
                self.dimension_names[value].append(n)
        elif isinstance(value, Unit):
            super().add(value)
            self.units.setdefault(value.dim, [])
            self.units[value.dim].append(value)

            if value.symbols:
                for n in self.dimension_names.get(value.dim, []):
                    self.dimension_symbol[n] = value.symbol
        elif isinstance(value, UnitSet):
            for units in value.units.values():
                self.add(units[-1])

        return value

    __call__ = add

    def remove(
        self,
        value: 'Unit | Dimension | UnitSet',
        *names: str
    ):
        if isinstance(value, Dimension):
            self.dimension_names.setdefault(value, [])
            for n in names:
                if n in self.dimension_names[value]:
                    self.dimension_names[value].remove(n)
        elif isinstance(value, Unit):
            super().remove(value)
            self.units.setdefault(value.dim, [])
            if value in self.units[value.dim]:
                self.units[value.dim].remove(value)
        elif isinstance(value, UnitSet):
            for units in value.units.values():
                self.unregister(*units)

    # helper functions

    def register(self, *units: Unit):
        for unit in units:
            self.add(unit)

    def unregister(self, *units: Unit):
        for unit in units:
            self.remove(unit)


display = UnitSet()
