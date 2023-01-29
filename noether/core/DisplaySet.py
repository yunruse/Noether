'''
List of units used for display purposes.

Also handles dimension names.
'''

from typing import Union
from .Dimension import Dimension
from .Unit import Unit


class DisplaySet:
    units: dict[Dimension, list[Unit]]
    dimension_names: dict[Dimension, list[str]]

    dimension_symbol = dict[str, str]

    def __init__(self, *items: list[Unit]):
        self.units = dict()
        self.dimension_names = dict()
        self.dimension_symbol = dict(dimensionless='')
        self.register(*items)

    def __repr__(self):
        return 'DisplaySet({})'.format(', '.join(
            str(i[-1]) for i in self.units.values()
        ))

    def add(self, value: Union[Unit, Dimension], *names: list[str]):
        if isinstance(value, Dimension):
            self.dimension_names.setdefault(value, [])
            for n in names:
                self.dimension_names[value].append(n)
        elif isinstance(value, Unit):
            self.units.setdefault(value.dim, [])
            self.units[value.dim].append(value)

            if value.symbols:
                for n in self.dimension_names.get(value.dim, []):
                    self.dimension_symbol[n] = value.symbol

        return value

    __call__ = add

    def remove(self, value: Union[Unit, Dimension], names: list[str]):
        if isinstance(value, Dimension):
            self.dimension_names.setdefault(value, [])
            for n in names:
                if n in self.dimension_names[value.dim]:
                    self.dimension_names[value.dim].remove(n)
        elif isinstance(value, Unit):
            self.units.setdefault(value.dim, [])
            if value in self.units[value.dim]:
                self.units[value.dim].remove(value)

    def register(self, *units: list[Unit]):
        for unit in units:
            self.add(unit)

    def unregister(self, *units: list[Unit]):
        for unit in units:
            self.remove(unit)


display = DisplaySet()
