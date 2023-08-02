from math import log10
from noether.helpers import Real

from ...errors import IncompatibleUnitError
from ..Measure import Measure
from ..Unit import Unit


class LogarithmicUnit(Unit):
    "A logarithmic unit, such as the decibel."
    unit: Measure
    units_per_ten: Real

    def __init__(
        self,
        unit: Measure,
        units_per_ten: Real,
        names: list[str] | str | None = None,
        symbols: list[str] | str | None = None,
    ):
        object.__setattr__(self, 'unit', unit)
        object.__setattr__(self, 'units_per_ten', units_per_ten)
        Unit.__init__(self, unit, names, symbols)

    def __call__(self, value: Real | Unit):
        if isinstance(value, Unit):
            # ensure .unit is a Unit if possible
            unit = value if self.unit == 1 else self.unit * value
            return LogarithmicUnit(
                unit, self.units_per_ten,
                f'{self.name}({value.name})', f'{self.symbol}({value.symbol})')
        else:
            val = self.unit * 10 ** (value / self.units_per_ten)
            return val @ self

    def __cannot_operate(self, *args):
        raise TypeError(
            'Cannot operate on a LogarithmicUnit - you must call it e.g.'
            f' {self.symbol}(3)')

    __mul__ = __add__ = __sub__ = __truediv__ = __floordiv__ = __cannot_operate  # type: ignore

    def __and__(self, _: Unit):
        raise IncompatibleUnitError(
            'A logarithmic unit {self} cannot be composed with other units!')

    __rand__ = __and__

    def _repr_measure(self, measure: Real | Measure):
        v: Real = measure._value if isinstance(
            measure, Measure) else measure  # type: ignore
        if v <= 0:
            raise ValueError(
                'LogarithmicUnits can only be used on positive units')
        return Unit._repr_measure(self, log10(v / self._value) * self.units_per_ten)

    def _json_extras(self):
        return {'units_per_ten': self.units_per_ten}
