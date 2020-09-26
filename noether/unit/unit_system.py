from .dimension import Dimension
from .measure import Measure

# TODO: add unit display layer system
# This MUST be used, eventually, so that Unit.display follows the order of:
# - fundamental SI units
# - SI derived units
# - whatever the user does display() on
# This layered system will not only clean up code, but make it much more interchangeable.


class UnitSystem:
    _mapping: dict
    fundamental: bool = False
    '''
    A unit system, mapping a dimension to a unit.
    
    Acts somewhat like a `dict` in terms of API.
    Instantiate with a list of units.
    To add or replace a unit, use system.use(unit);
    to revert, use system.revert(unit_or_dim).

    Use system.display() (or, display(system) in Noether's REPL)
    to change the units displayed by Noether.
    
    If a system has the "fundamental" flag set, any unit provided of
    a fundamental dimension (eg the metre) will be used for dimensions
    without an explicitly-named unit (eg area: metre**2)
    '''

    def __len__(self):
        return len(self._mapping)

    def __iter__(self):
        for unit in self._mapping.values():
            yield unit

    def __getitem__(self, dim: Dimension):
        if isinstance(dim, Measure):
            # this isn't official API, but will fix user blunders
            dim = dim.dim
        if not isinstance(dim, Dimension):
            raise TypeError('System can only be indexed by dimension.')
        # TODO: display derived units eg inch**2
        return self._mapping.get(dim)

    def __repr__(self):
        return '{}({})'.format(
            type(self).__name__,
            ', '.join(unit.symbols[0] for unit in self)
        )

    def __init__(self, *units, fundamental=False):
        self._mapping = {u.dim: u for u in units}
        self.fundamental = fundamental

    def use(self, unit):
        mapping = {u.dim: u for u in self}
        mapping[unit.dim] = unit

    def revert(self, unit):
        del mapping[unit.dim]
