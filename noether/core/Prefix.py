'''
Prefixes a unit may take.
'''

from typing import TYPE_CHECKING, TypeVar, Generic
from dataclasses import dataclass

from ..helpers import MeasureValue

if TYPE_CHECKING:
    from . import Measure

T = TypeVar('T', int, MeasureValue)


@dataclass(frozen=True)
class Prefix(Generic[T]):
    prefix: str
    symbol: str
    value: T
    display: bool = True

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError('Prefixes must be positive!')

    def __json__(self):
        return {
            'prefix': self.prefix,
            'symbol': self.symbol,
            'value': self.value,
            'display': self.display
        }

    def _geo(self, measure: 'Measure | Prefix | T', direction: int):
        from . import Unit, PrefixedUnit

        if isinstance(measure, Prefix):
            measure = measure.value
        if direction == -1:
            measure = 1 / measure

        if isinstance(measure, Unit):
            if not isinstance(measure, PrefixedUnit):
                return PrefixedUnit(self, measure)

        return self.value * measure

    def __mul__(self, measure: 'Measure | Prefix'):
        return self._geo(measure, +1)

    def __truediv__(self, measure: 'Measure | Prefix'):
        return self._geo(measure, -1)
