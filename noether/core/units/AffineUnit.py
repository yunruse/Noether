from noether.helpers import Real

from ...errors import DimensionError, IncompatibleUnitError
from ..Measure import Measure
from ..Unit import Unit


class AffineUnit(Unit):
    "Unit with a zero-point. Useful for e.g. temperature."
    zero_point: Measure

    def __init__(
        self,
        unit: Measure,
        zero_point: Measure,
        names: list[str] | str | None = None,
        symbols: list[str] | str | None = None,
        info: str | None = None,
    ):
        DimensionError.check(zero_point.dim, unit.dim, '(AffineUnit creation)')
        object.__setattr__(self, 'zero_point', zero_point)
        Unit.__init__(
            self, unit,
            names=names, symbols=symbols, info=info)

    def __call__(self, value: Real, stddev: Real | None = None):
        return Measure.__call__(self, value, stddev) + self.zero_point

    def __and__(self, _: Unit):
        raise IncompatibleUnitError(
            'An affine unit {self} cannot be composed with other units!')

    # TODO: what about * and / .....?

    __rand__ = __and__

    def _repr_measure(self, measure: Measure):
        return Unit._repr_measure(self, measure - self.zero_point)

    def _json_extras(self):
        return {'zero_point': self.zero_point._value}
