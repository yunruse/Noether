
from typing import TYPE_CHECKING

from noether.errors import DimensionError
from noether.config import conf
from .Measure import OPENLINEAR, Measure

if TYPE_CHECKING:
    from .Unit import Unit


class MeasureRelative(Measure):
    '''
    A Measure with a custom Unit for display.
    >>> meter @ cm
    100 cm  # length
    '''

    __slots__ = ('_value', 'stddev', 'dim', 'unit')
    unit: 'Unit'

    @property
    def value(self):
        return self._value / self.unit._value

    def __init__(self, measure: Measure, unit: 'Unit'):
        Measure.__init__(self, measure)
        object.__setattr__(self, 'unit', unit)

    def display_unit(self):
        if self.dim != self.unit.dim and not conf.get(OPENLINEAR):
            raise DimensionError(
                self.dim, self.unit.dim,
                f"To use @ on units with different dimensions, enable conf.{OPENLINEAR}.")

        return self.unit

    # HACK: syntactic sugar such that @ "binds looser"

    def __and__(self, other: 'Unit'):
        return MeasureRelative(self, self.unit & other)

    def __mul__(self, other: 'Unit'):
        return MeasureRelative(self, self.unit * other)  # type: ignore

    def __truediv__(self, other: 'Unit'):
        return MeasureRelative(self, self.unit / other)  # type: ignore
