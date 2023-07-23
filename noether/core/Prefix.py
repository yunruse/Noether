'''
Prefixes a unit may take.
'''

from typing import TYPE_CHECKING, Iterable, TypeVar, Generic
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

    def __json__(self):
        return {
            'prefix': self.prefix,
            'symbol': self.symbol,
            'value': self.value
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


class PrefixSet(set[Prefix]):
    __slots__ = ('name', )

    def __init__(self, name: str, prefixes: Iterable[Prefix] | None = None):
        self.name = name
        super().__init__(prefixes or [])

    def __or__(self, other: 'PrefixSet'):
        return PrefixSet(
            f'{self.name} | {other.name}',
            set(self) | set(other))

    def __repr__(self):
        return f'PrefixSet({self.name!r}, {set(self)!r})'

    def __json__(self):
        return {'name': self.name, 'prefixes': [p.__json__() for p in self]}
