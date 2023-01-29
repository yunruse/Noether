from numbers import Real
from ..errors import DimensionError, IncompatibleUnitError
from .Measure import Measure
from .Unit import Unit


class AffineUnit(Unit):
    zero_point: Measure

    def __init__(
        self,
        unit: Measure,
        zero_point: Measure,
        names: list[str] | str | None = None,
        symbols: list[str] | str | None = None,
    ):
        if unit.dim != zero_point.dim:
            raise DimensionError(
                f'Cannot use {zero_point.dim} as zero-point dimension'
                f' when unit provided has dimension {zero_point.dim}')
        object.__setattr__(self, 'zero_point', zero_point)
        Unit.__init__(self, unit, names, symbols)

    def __call__(self, value: Real, stddev: Real | None = None):
        return Measure.__call__(self, value, stddev) + self.zero_point

    def __and__(self, _: Unit):
        raise IncompatibleUnitError(
            'AffineUnit {self} cannot be chained with units.')

    __rand__ = __and__

    def repr_measure(self, measure: Measure):
        return Unit.repr_measure(self, measure - self.zero_point)

    def _json_extras(self):
        return {'zero_point': self.zero_point / self.value}