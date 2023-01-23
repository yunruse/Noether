
from typing import TYPE_CHECKING
from .Measure import Measure

if TYPE_CHECKING:
    from .Unit import Unit


class MeasureRelative(Measure):
    '''
    A Measure with a custom Unit for display.
    >>> meter @ cm
    100 cm <length>
    '''

    __slots__ = ('value', 'stddev', 'dim', 'unit')
    unit: 'Unit'

    def __init__(self, measure: Measure, unit: 'Unit'):
        Measure.__init__(self, measure)
        object.__setattr__(self, 'unit', unit)

    def display_unit(self):
        return self.unit

    def __and__(self, other: 'Unit'):
        # @ binds tighter than &, so correct for this
        return MeasureRelative(self, self.unit & other)
