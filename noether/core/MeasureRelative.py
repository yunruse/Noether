
from typing import TYPE_CHECKING, Optional, TypeVar

from ..helpers import MeasureValue
from ..errors import DimensionError
from .Measure import Measure

if TYPE_CHECKING:
    from .Unit import Unit


T = TypeVar('T', int, MeasureValue)

class MeasureRelative(Measure[T]):
    '''
    A Measure with a custom Unit for display.
    >>> meter @ cm
    100 cm  # length
    '''


    def __init__(self, measure: Measure, unit: 'Unit'):
        Measure.__init__(self, measure)
        object.__setattr__(self, 'unit', unit)
        # HACK: see below
        # self.__verify_dim('compose')

    __slots__ = ('_value', 'stddev', 'dim', 'unit')
    unit: 'Unit'

    @property
    def value(self) -> T:
        DimensionError.check(self.dim, self.unit.dim)
        from .units import AffineUnit
        value = self._value
        if isinstance(self.unit, AffineUnit):
            value -= self.unit.zero_point._value

        return value / self.unit._value

    def _casting_value(self):
        return self.value

    def display_unit(self):
        DimensionError.check(self.dim, self.unit.dim)
        return self.unit

    def __round__(self, ndigits: Optional[int] = None):
        # we can round 'relative' to a unit
        return self.unit(
            round(self._casting_value(), ndigits),
            # TODO: handle uncertainty
        )

    # HACK: syntactic sugar such that @ appears to bind more loosely,
    # so `measure @ a&b` or `measure @ a*b` or `measure @ a/b` work.
    # This obviously means we only check a MeasureRelative when used
    # and when not composed. I am a tiny bit unsure if this is good practice.

    def __and__(self, other: 'Unit'):
        return MeasureRelative(self, self.unit & other)

    def __mul__(self, other: 'Unit'):
        return MeasureRelative(self, self.unit * other)  # type: ignore

    def __truediv__(self, other: 'Unit'):
        return MeasureRelative(self, self.unit / other)  # type: ignore
