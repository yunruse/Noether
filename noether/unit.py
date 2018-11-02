'''Noether: International System of Units dimensionality object'''

import math
import operator

from .helpers import intify, sign, product
from .scale import *
from .matrix import Matrix

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
    __slots__ = 'dim delta symbols'.split()
    
    precision = 3
    showUnits = True
    showDimension = True
    openLinear = False
    
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
        
        if self.delta:
            sDelta = scinot(self.delta, self.precision)
            sNum += ' ± ' + sDelta
        
        return sNum, symbol, measure
    
    def __str__(self):
        sNum, symbol, measure = self._reprElements()
        
        if sNum == -1 and self.showUnits:
            sNum = '-'
        
        if not self.showUnits:
            return sNum.strip()
        
        if self.showDimension and measure:
            return sNum + symbol + ' (' + measure + ')'
        else:
            return sNum + symbol
    
    __repr__ = __str__
    
    def __new__(cls, value, *symbols,
                delta=None, _factor=1, measure=None):
        
        num = value if isinstance(value, (int, float)) else _factor
        dim = (0, 0, 0, 0, 0, 0, 0)
        
        if isinstance(value, Unit):
            dim = value.dim
            delta = value.delta if delta is None else delta
        elif isinstance(value, str):
            dim = tuple(int(d == value) for d in dimensions)
    
        self = float.__new__(cls, num)
        self.dim = dim
        self.delta = 0 if delta is None else abs(delta)
        self.symbols = symbols
        if measure is not None:
            # do not add unit if not given a symbol,
            # as only the measure name is introduced:
            # eg speed, area, etc
            self.displayMeasures[self.dim] = (
                measure, self if symbols else None)
    
        return self
    
    # Dimension-changing operators
    
    @property
    def invUnit(self):
        return Unit(
            tuple(-i for i in self.dim),
            _factor=float(self))
    
    @property
    def inv(self):
        return 1 / self
    
    def __mul__(self, other, f=float.__mul__, k=1):
        dim = self.dim
        un = self.delta
        
        if isinstance(other, Unit):
            dim = tuple(
                dim[i] + k * other.dim[i]
                for i in range(len(dimensions)))
            if float(self) == 0 or float(other) == 0:
                un = 0
            else:
                pun = un / float(self)
                pun += other.delta / float(other)
                pun += (un / float(self))
                un = other * pun
        else:
            un *= other
        
        return Unit(dim, delta=un,
                    _factor=f(self, float(other)))
    
    def __truediv__(self, other):
        return self.__mul__(other, float.__truediv__, k=-1)

    def __floordiv__(self, other):
        return self.__mul__(other, float.__floordiv__, k=-1)
    
    __rmul__ = __mul__
    
    def __pow__(self, exp):
        return Unit(
            tuple(intify(v*exp) for v in self.dim),
            delta = self.delta * abs(exp),
            _factor = float(self)**exp)

    def __rtruediv__(self, other):
        factor = float.__truediv__(float(other), float(self))
        return Unit(
            tuple(-v for v in self.dim),
            _factor=factor)
    
    # Linear operations
    
    __neg__ = lambda s: s * -1
    
    def __cmp(self, other):
        # Linear helper
        if (not self.openLinear
            and isinstance(other, Unit)
            and self.dim != other.dim):
            raise ValueError('Inequal units {} and {}.'.format(
                self.asFundamentalUnits(),
                other.asFundamentalUnits()))
        
        # Return limits of uncertainty
        sl = float(self) - self.delta
        su = float(self) + self.delta
        if isinstance(other, Unit):
            ol = float(other) - other.delta
            ou = float(other) + other.delta
        else:
            ol, ou = other, other
        return sl, su, ol, ou
    
    def __add__(self, other, op=operator.add):
        self.__cmp(other)
        odelta = other.delta if isinstance(other, Unit) else 0
        return Unit(
            self.dim,
            delta   = op(float(self.delta), odelta),
            _factor = op(float(self), other))
    
    def __sub__(self, other):
        self.__add__(other, operator.sub)
    
    __radd__ = __add__
    __rsub__ = __sub__
    
    # comparison operators require range-checking
    
    def __eq__(self, other):
        sl, su, ol, ou = self.__cmp(other)
        return ((sl <= ol <= su) or (sl <= ou <= su) or
                (ol <= sl <= ou) or (ol <= su <= ou))
    
    def __ne__(self, other):
        sl, su, ol, ou = self.__cmp(other)
        return sl <= ou or ol <= su
    
    #__lt__ = lambda s, o: s.__cmp(o, operator.lt)
    #__le__ = lambda s, o: s.__cmp(o, operator.le)
    #__ge__ = lambda s, o: s.__cmp(o, operator.ge)
    #__gt__ = lambda s, o: s.__cmp(o, operator.gt)
    
    # Matrix operators
    
    def __and__(self, other):
        return Matrix(self) & other
    def __rand__(self, other):
        return other & Matrix(self)
    
    def __or__(self, other):
        return Matrix(self) | other
    def __or__(self, other):
        return other | Matrix(self)