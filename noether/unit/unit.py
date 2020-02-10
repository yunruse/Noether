from .measure import Measure
from .dimension import Dimension

class Unit(Measure):
    '''
    Special kind of unit with a symbol.
    Vital for display and conversion.
    '''
    __slots__ = Measure.__slots__ + ["symbols", "names"]

    def __new__(cls, value, *a, symbols=None, names=None, is_display=False, **kw):
        if isinstance(value, Dimension):
            kw['dim'] = value
            value = 1
        self = Measure.__new__(cls, value, **kw)
        self.symbols = symbols or tuple()
        self.symbols += a
        self.names = names or tuple()

        if self.symbols and is_display:
            self._base_display_units[self.dim] = self
        return self
    
    def __repr__(self):
        if self == self.display_unit:
            if self.names:
                return self.names[0] + self._opt_dimension_name()
            elif self.symbols:
                return self.symbols[0] + self._opt_dimension_name()
        return Measure.__repr__(self)
