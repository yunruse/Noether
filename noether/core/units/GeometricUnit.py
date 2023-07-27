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

    @staticmethod
    def _resolve_unit(u: Unit):
        from .LinearUnit import LinearUnit
        if isinstance(u, LinearUnit):
            u = u.units[-1]

        if isinstance(u, GeometricUnit):
            return u.units
        return u

    def __mul__(self, value: Unit):
        if isinstance(value, Unit):
            return type(self)(self.units * self._resolve_unit(value))
        return Measure.__mul__(self, value)

    def __truediv__(self, value: Unit):
        if isinstance(value, Unit):
            return type(self)(self.units / self._resolve_unit(value))
        return Measure.__truediv__(self, value)

    def __pow__(self, exponent: Rational):
        return type(self)(self.units ** exponent)

    @property
    def name(self):
        return self.units.display(key=lambda q: (-q[1], q[0].dim.order))

    @property
    def symbol(self):
        return self.units.display(
            lambda x: x.symbol,
            key=lambda q: (-q[1], q[0].dim.order),
            drop_multiplication_signs=True)
