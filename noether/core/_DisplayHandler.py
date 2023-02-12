
from typing import TypeVar
from .Unit import Unit
from .UnitSet import UnitSet
from .Dimension import Dimension


class DisplayHandler:
    '''
    Internal class used to provide names and units
    to various dimensions.
    '''

    dimension_units: dict[Dimension, list[Unit]]
    dimension_names: dict[Dimension, list[str]]
    dimension_symbol: dict[str, str]

    def __init__(self, *items: Unit):
        self.dimension_units = dict()
        self.dimension_names = dict()
        self.dimension_symbol = dict(dimensionless='')

        self.displays(*items)

    T = TypeVar('T', Unit, Dimension, 'UnitSet')

    def display(self, value: T, *names: str) -> T:
        if isinstance(value, Dimension):
            self.dimension_names.setdefault(value, [])
            for n in names:
                self.dimension_names[value].append(n)
        elif isinstance(value, Unit):
            self.dimension_units.setdefault(value.dim, [])
            self.dimension_units[value.dim].append(value)

            if value.symbols:
                for n in self.dimension_names.get(value.dim, []):
                    self.dimension_symbol[n] = value.symbol
        elif isinstance(value, UnitSet):
            for unit in value:
                self.display(unit)

        return value

    __call__ = display

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
            self.dimension_units.setdefault(value.dim, [])
            if value in self.dimension_units[value.dim]:
                self.dimension_units[value.dim].remove(value)
        elif isinstance(value, UnitSet):
            for unit in value:
                self.remove(unit)

    # helper functions

    def displays(self, *units: Unit):
        for unit in units:
            self.display(unit)

    def removes(self, *units: Unit):
        for unit in units:
            self.remove(unit)


display = DisplayHandler()
