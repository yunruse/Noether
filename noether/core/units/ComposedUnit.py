from math import prod
from noether.helpers import Rational

from ...Multiplication import Multiplication
from ..Measure import Measure
from ..Unit import Unit


class ComposedUnit(Unit):
    "Multiplication, division and exponentiation of other units. For example, meter / second."
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
            value = value.units if isinstance(value, ComposedUnit) else value
            return type(self)(self.units * value)
        return Measure.__mul__(self, value)

    def __truediv__(self, value: Unit):
        if isinstance(value, Unit):
            value = value.units if isinstance(value, ComposedUnit) else value
            return type(self)(self.units / value)
        return Measure.__truediv__(self, value)

    def __pow__(self, exponent: Rational):
        return type(self)(self.units ** exponent)

    def _display_element(self):
        return self.units.display()

    def __str__(self):
        return self.units.display()

    def unit_to_display(self):
        return self.units.display(lambda x: x.symbol)
