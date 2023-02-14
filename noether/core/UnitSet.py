'''
List of units used for display purposes.

Also handles dimension names.
'''

from typing import Iterable
from .Unit import Unit
from .Dimension import Dimension


class UnitSet(set[Unit]):
    '''
    set[Unit] with convenience functions.

    Useful for display
    '''

    def __init__(self, iterable: 'Iterable[Unit | UnitSet]' = []):
        ""
        super().__init__()
        for x in iterable or {}:
            if isinstance(x, Unit):
                self.add(x)
            else:
                self |= x

    def __hash__(self):
        return hash(tuple(self))

    def add(self, value: Unit) -> Unit:
        "Adds and also returns value."
        super().add(value)
        return value

    # Dimension getter

    def unique_on_dimensions(self):
        "True iff no unit shares a dimension."
        dims_seen: set[Dimension] = set()
        for unit in self:
            if unit.dim in dims_seen:
                return False
            dims_seen.add(unit.dim)
        return True

    def unit_for_dimension(self, dim: Dimension) -> Unit | None:
        for unit in self:
            if unit.dim == dim:
                return unit

    __call__ = add
