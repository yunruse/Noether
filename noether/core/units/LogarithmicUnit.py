from math import log10
from noether.helpers import Real

from ...errors import IncompatibleUnitError
from ..Measure import Measure
from ..Unit import Unit


class LogarithmicUnit(Unit):
    "A logarithmic unit, such as the decibel."
    unit: Real | Measure
    units_per_ten: Real

    def __init__(
        self,
        unit: Real | Measure,
        units_per_ten: Real,
        names: list[str] | str | None = None,
        symbols: list[str] | str | None = None,
        info: str | None = None,
    ):
        object.__setattr__(self, 'unit', unit)
        object.__setattr__(self, 'units_per_ten', units_per_ten)
        # ensure unit == unit
        Unit.__init__(
            self, unit * 10 ** (1/units_per_ten),
            names=names, symbols=symbols, info=info)

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

    def __and__(self, _: Unit):
        raise IncompatibleUnitError(
            'A logarithmic unit {self} cannot be composed with other units!')

    __rand__ = __and__

    def _repr_measure(self, measure: Real | Measure):
        V = Measure._extract_value
        m = V(measure)
        if m <= 0:
            raise ValueError(
                'LogarithmicUnits can only be used on positive units')
        return Unit._repr_measure(
            self, log10(m / V(self.unit)) * self.units_per_ten)

    def _json_extras(self):
        V = Measure._extract_value
        return {'value': V(self.unit), 'units_per_ten': self.units_per_ten}
