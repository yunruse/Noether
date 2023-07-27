
from typing import TypeVar
from .Unit import Unit
from .UnitSet import UnitSet
from .Dimension import Dimension


class DisplayHandler:
    '''
    Internal class used to provide names and units
    to various dimensions.
    '''

    dimensions: set[Dimension]
    dimension_units: dict[Dimension, list[Unit]]
    _dimension_symbol: dict[str, str]  # HACK

    def __init__(self, *items: Unit):
        self.dimensions = set()
        self.dimension_units = dict()
        self._dimension_symbol = dict(dimensionless='')

        self.displays(*items)

    T = TypeVar('T', Unit, Dimension, 'UnitSet')

    def dimension_unit(self, dim: Dimension):
        units = self.dimension_units.get(dim, [])
        if units:
            return units[-1]

        from noether.core.units import GeometricUnit, LinearUnit
        from .Dimension import BaseDimension

        def resolve(d: BaseDimension):
            d2 = display.dimension_units[Dimension(d)][-1]
            if isinstance(d2, LinearUnit):
                return d2.units[-1]
            return d2

        return GeometricUnit({
            resolve(d): exp
            for d, exp in dim.items()
        })

    def display(self, value: T) -> T:
        if isinstance(value, Dimension):
            self.dimensions.add(value)

        elif isinstance(value, Unit):
            self.dimension_units.setdefault(value.dim, [])
            self.dimension_units[value.dim].append(value)
            if value.symbols:
                for n in value.dim.names:
                    self._dimension_symbol[n] = value.symbol
        elif isinstance(value, UnitSet):
            for unit in value:
                self.display(unit)

        return value

    __call__ = display

    def remove(
        self,
        value: 'Unit | Dimension | UnitSet',
    ):
        if isinstance(value, Dimension):
            self.dimensions.remove(value)
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
