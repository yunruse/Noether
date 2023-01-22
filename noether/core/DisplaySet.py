from .Dimension import Dimension
from .Unit import Unit


class DisplaySet:
    units: dict[Dimension, list[Unit]]
    dimension_names: dict[Dimension, list[str]]

    def __init__(self):
        self.units = dict()
        self.dimension_names = dict()

    def register(self, value: Unit | Dimension, *names: list[str]):
        if isinstance(value, Dimension):
            self.dimension_names.setdefault(value, [])
            for n in names:
                self.dimension_names[value].append(n)
        elif isinstance(value, Unit):
            self.units.setdefault(value.dim, [])
            self.units[value.dim].append(value)

        return value

    __call__ = register

    def unregister(self, value: Unit | Dimension, names: list[str]):
        if isinstance(value, Dimension):
            self.dimension_names.setdefault(value, [])
            for n in names:
                if n in self.dimension_names[value.dim]:
                    self.dimension_names[value.dim].remove(n)
        elif isinstance(value, Unit):
            self.units.setdefault(value.dim, [])
            if value in self.units[value.dim]:
                self.units[value.dim].remove(value)


display = DisplaySet()