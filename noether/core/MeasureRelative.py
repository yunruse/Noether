
from typing import TYPE_CHECKING, Optional, TypeVar

from ..helpers import MeasureValue
from ..errors import DimensionError
from ..config import conf
from .Measure import OPENLINEAR, Measure

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
    
    def __verify_dim(self, verb: str):
        if not conf.get(OPENLINEAR):
            DimensionError.check(
                self.dim, self.unit.dim,
                f"Cannot {verb} MeasureRelative (measure @ unit) in this way; it is ambiguous."
                f" To enable this anyway, enable setting conf.{OPENLINEAR}.")


    __slots__ = ('_value', 'stddev', 'dim', 'unit')
    unit: 'Unit'

    @property
    def value(self) -> T:
        self.__verify_dim('utilise')
        from .units import AffineUnit
        value = self._value
        if isinstance(self.unit, AffineUnit):
            value -= self.unit.zero_point._value

        return value / self.unit._value

    def _casting_value(self):
        return self.value

    def display_unit(self):
        self.__verify_dim('display')
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
