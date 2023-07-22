from math import prod
from noether.helpers import Rational

from ...Multiplication import Multiplication
from ..Measure import Measure
from ..Unit import Unit


class GeometricUnit(Unit):
    '''
    A geometric composition of units, like `meter / second ** 2`.

    Useful for display purposes.
    '''

    units: Multiplication[Unit]

    def __init__(self, unit_or_dict: Unit | dict[Unit, Rational]):
        if isinstance(unit_or_dict, dict):
            units = Multiplication(unit_or_dict)
            product = prod(Measure(x) ** e for x, e in units.items())
            unit: Unit = product  # type: ignore
        else:
            unit = unit_or_dict
            units = Multiplication(unit)

        super().__init__(unit)
        object.__setattr__(self, 'units', units)

    def __mul__(self, value: Unit):
        if isinstance(value, Unit):
            v = value.units if isinstance(value, GeometricUnit) else value
            return type(self)(self.units * v)
        return Measure.__mul__(self, value)

    def __truediv__(self, value: Unit):
        if isinstance(value, Unit):
            v = value.units if isinstance(value, GeometricUnit) else value
            return type(self)(self.units / v)
        return Measure.__truediv__(self, value)

    def __pow__(self, exponent: Rational):
        return type(self)(self.units ** exponent)

    @property
    def name(self):
        return self.units.display()

    @property
    def symbol(self):
        return self.units.display(lambda x: x.symbol)
