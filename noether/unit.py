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
    __slots__ = 'dim _delta _epsilon symbols'.split()
    
    def __new__(cls, value, *symbols,
                _delta=None, _epsilon=None, _factor=1, measure=None):
        
        num = _factor
        dim = (0, 0, 0, 0, 0, 0, 0)
        
        if isinstance(value, Unit):
            dim = value.dim
            if _delta is None:
                _delta = value._delta
            if _epsilon is None:
                _epsilon = value._epsilon
        elif isinstance(value, str):
            dim = tuple(int(d == value) for d in dimensions)
        elif isinstance(value, (int, float)):
            num = value
        elif isinstance(value, tuple):
            dim = value
    
        self = float.__new__(cls, num)
        self.dim = dim
        self._delta = None
        self._epsilon = None
        if _delta is not None:
            self._delta = abs(_delta)
        elif _epsilon is not None:
            self._epsilon = abs(_epsilon)
        else:
            self._delta = 0
        
        self.symbols = symbols
        if measure is not None:
            # do not add unit if not given a symbol,
            # as only the measure name is introduced:
            # eg speed, area, etc
            self.displayMeasures[self.dim] = (
                measure, self if symbols else None)
    
        return self
    
    @property
    def epsilon(self):
        if self._epsilon is not None:
            return self._epsilon
        d, f = self._delta, float(self)
        if d == 0 or f == 0:
            return 0
        else:
            return d / f
    
    @epsilon.setter
    def _set_epsilon(self, n):
        self._epsilon = n
        self._delta = None
    
    @property
    def delta(self):
        if self._delta is not None:
            return self._delta
        e, f = self._epsilon, float(self)
        if e == 0 or f == 0:
            return 0
        else:
            return e * f
    
    @epsilon.setter
    def _set_delta(self, n):
        self._delta = n
        self._epsilon = None
    
    precision = 3
    showUnits = True
    showDimension = True
    openLinear = False
    unicodeExponent = True
    
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
    
    def _symbolMeasure(self):
        num = self.real
        measure, bUnit = self._measureUnit()
        if bUnit and bUnit != self:
            num /= bUnit.real
        
        if bUnit:
            symbol = bUnit.symbols[0]
        else:
            symbol = self.asFundamentalUnits()
        
        return symbol, measure
    
    def _numerical(self, symbol=False):
        n, d = float(self), self.delta
        eN, mN = exp_mantissa(n)
        eD, mD = exp_mantissa(d)
        
        if d:
            exp = max(eN, eD)
            dExp = abs(eN - eD)
            
            fuzzy = (dExp < 4 and not (
                -3 < exp < 2))
            if fuzzy:
                Q = 10 ** exp
                n /= Q
                d /= Q
        else:
            exp = eN
            fuzzy = not (-3 < eN < 2)
            if fuzzy:
                n = mN
        
        n, d = intify(n), intify(d)
        if exp and fuzzy:
            if self.unicodeExponent:
                sExp = '×10' + str(exp).translate(powerify)
            else:
                sExp = '×10^' + str(exp)
        else:
            sExp = ''
        
        if fuzzy:
            sNum = str(round(n, self.precision))
            sDelta = str(round(d, self.precision))
        else:
            sNum = scinot(n, self.precision, self.unicodeExponent)
            sDelta = scinot(d, self.precision, self.unicodeExponent)
        
        if d:
            sNum += ' ± ' + sDelta
            if symbol or sExp:
                sNum = '(' + sNum + ')'
        
        return sNum + sExp
    
    def __str__(self):
        symbol, measure = self._symbolMeasure()
        sNum = self._numerical(symbol)
        
        if not self.showUnits:
            return sNum.strip()
        
        if sNum == '-1':
            sNum = '-'
        
        if self.showDimension and measure:
            return sNum + symbol + ' (' + measure + ')'
        else:
            return sNum + symbol
    
    __repr__ = __str__
    
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
        fo = float(other)
        
        if isinstance(other, Unit):
            dim = tuple(
                dim[i] + k * other.dim[i]
                for i in range(len(dimensions)))
            if float(self) == 0 or fo == 0:
                _e = 0
            else:
                _e = self.epsilon * other.epsilon
        else:
            _e = self.epsilon
        
        return Unit(
            dim, _epsilon=_e,
            _factor=f(self, fo))
    
    __call__ = __mul__
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        return self.__mul__(other, float.__truediv__, k=-1)

    def __floordiv__(self, other):
        return self.__mul__(other, float.__floordiv__, k=-1)
    
    def __pow__(self, exp):
        return Unit(
            tuple(intify(v*exp) for v in self.dim),
            _epsilon = self.epsilon * abs(exp),
            _factor = float(self) ** exp
        )

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
            _delta  = op(float(self.delta), odelta),
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