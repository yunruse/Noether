'''Noether: International System of Units dimensionality object'''

import math
import operator
from .helpers import intify, sign
from .scale import *

dimensions = {
    'length': 'm',
    'time': 's',
    'current': 'A',
    'temperature': 'K',
    'mass': 'Kg',
    'luminosity': 'Cd',
    'substance': 'mol'
}

class UnitMeta(type):
    def _dU_get(cls):
        return list(cls._displayUnits.values())
    
    def _dU_set(cls, bases):
        cls._displayUnits.clear()
        if not hasattr(bases, '__iter__'):
            bases = [bases]
        for unit in bases:
            cls._displayUnits[unit.dim] = unit
    
    def _dU_del(cls):
        cls._displayUnits.clear()
    
    displayUnits = property(_dU_get, _dU_set, _dU_del)

class Unit(float, metaclass=UnitMeta):
    __slots__ = 'dim symbols'.split()
    
    precision = 3
    showUnits = True
    showDimension = True
    
    # Display dictionaries
    
    # Used to obtain symbol and measure.
    # The unit is used so repr(Joule) doesn't just
    # respond with a remarkably useless `1J (energy)`
    # {unit.dim: (measure_name, base_unit or None}
    displayMeasures = {}
    
    # Base units to display relative to.
    # {unit.dim: Unit}
    _displayUnits = {}
    
    def _measureUnit(self):
        if all(i == 0 for i in self.dim):
            return 'unitless', None
        
        measure, base_unit = self.displayMeasures.get(
            self.dim, (None, None))
        
        base_unit = self._displayUnits.get(self.dim, base_unit)
        return measure, base_unit

    @property
    def measure(self):
        return self._measureUnit()[0]

    @property
    def baseUnit(self):
        return self._measureUnit()[1]

    def asFundamentalUnits(self):
        dims = []
        for i, sym in enumerate(dimensions.values()):
            v = self.dim[i]
            if v == 0:
                continue
            elif v != 1:
                sym += str(v).translate(powerify)
            dims.append(sym)
        
        return '·'.join(dims)
    
    def _reprElements(self):
        num = self.real
        measure, bUnit = self._measureUnit()
        if bUnit and bUnit != self:
            num /= bUnit.real
        
        if bUnit:
            symbol = bUnit.symbols[0]
        else:
            symbol = self.asFundamentalUnits()

        sNum = scinot(num, self.precision)
        if num != int(num):
            sNum += ' '
        
        return sNum, symbol, measure
    
    def __repr__(self):
        sNum, symbol, measure = self._reprElements()
        
        if sNum == -1 and self.showUnits:
            sNum = '-'
        
        if not self.showUnits:
            return sNum.strip()
        
        if self.showDimension:
            return sNum + symbol + ' (' + measure + ')'
        else:
            return sNum + symbol
    
    def __new__(cls, dim, *symbols, _factor=1, measure=None):
        num = dim if isinstance(dim, Unit) else _factor
        
        if isinstance(dim, Unit):
            dim = dim.dim
        elif isinstance(dim, str):
            dim = tuple(int(d == dim) for d in dimensions)

        self = float.__new__(cls, num)
        self.dim = dim
        self.symbols = symbols
        if measure is not None:
            # do not add unit if not given a symbol,
            # as only the measure name is introduced:
            # eg speed, area, etc
            self.displayMeasures[self.dim] = (
                measure, self if symbols else None)

        return self

    # Dimension-changing operators

    def __mul__(self, other, f=float.__mul__, k=1):
        dim = self.dim
        if isinstance(other, Unit):
            dim = tuple(
                self.dim[i] + k * other.dim[i]
                for i in range(len(dimensions)))
        
        return Unit(dim, _factor=f(float(self), float(other)))

    def __truediv__(self, other):
        return self.__mul__(other, float.__truediv__, k=-1)

    def __floordiv__(self, other):
        return self.__mul__(other, float.__floordiv__, k=-1)

    __rmul__ = __mul__

    def __pow__(self, exp):
        factor = float.__pow__(self, exp)
        return Unit(
            tuple(intify(v*exp) for v in self.dim),
            _factor=factor)

    def __rtruediv__(self, other):
        factor = float.__truediv__(float(other), float(self))
        return Unit(
            tuple(-v for v in self.dim),
            _factor=factor)

    # Linear operations
    
    __neg__ = lambda s: Unit(s.dim, _factor=-float(s))

    def __cmp(self, other, f):
        if isinstance(other, Unit) and self.dim != other.dim:
            raise ValueError('Inequal units {} and {}.'.format(
                self.asFundamentalUnits(), other.asFundamentalUnits()))
        
        return f(self.real, other.real)
    
    __eq__ = lambda s, o: s.__cmp(o, operator.eq)
    __ne__ = lambda s, o: s.__cmp(o, operator.ne)
    __lt__ = lambda s, o: s.__cmp(o, operator.lt)
    __le__ = lambda s, o: s.__cmp(o, operator.le)
    __ge__ = lambda s, o: s.__cmp(o, operator.ge)
    __gt__ = lambda s, o: s.__cmp(o, operator.gt)
    
    __add__ = __radd__ = lambda s, o: Unit(s.dim, _factor=s.__cmp(o, operator.add))
    __sub__ = __rsub__ = lambda s, o: Unit(s.dim, _factor=s.__cmp(o, operator.sub))