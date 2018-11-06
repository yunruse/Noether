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

_emptyDim = (0, 0, 0, 0, 0, 0, 0)

class Unit(float, metaclass=UnitMeta):
    __slots__ = 'dim _delta _epsilon'.split()
    
    def __new__(cls, value=1, **kw):
        
        if isinstance(value, Unit):
            d = kw.setdefault
            d('_dim', value.dim)
            d('_delta', value._delta)
            d('_epsilon', value._epsilon)
            value = float(value)
    
        self = float.__new__(cls, value)
        
        dim = kw.get('_dim', (0, 0, 0, 0, 0, 0, 0))
        if isinstance(dim, str):
            dim = tuple(int(d == dim) for d in dimensions)
        self.dim = dim
        
        self._delta = kw.get('_delta', None)
        self._epsilon = kw.get('_epsilon', None)
    
        return self
    
    # Delta / epsilon (absolute / relative uncertainties)
    
    def _d_get(self):
        if self._delta is not None:
            return self._delta
        e, f = self._epsilon or 0, float(self)
        if e == 0 or f == 0:
            return 0
        else:
            return e * f
    def _d_set(self, d):
        self._delta = abs(d)
        self._epsilon = None
    delta = property(_d_get, _d_set, lambda s: s._d_set(0))
    
    def _e_get(self):
        if self._epsilon is not None:
            return self._epsilon
        d, f = self._delta or 0, float(self)
        if d == 0 or f == 0:
            return 0
        else:
            return d / f
    def _e_set(self, e):
        self._epsilon = abs(e)
        self._delta = None
    epsilon = property(_e_get, _e_set, lambda s: s._e_set(0))
    
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
                e = 0
            else:
                e = self.epsilon + other.epsilon
        else:
            e = self.epsilon
        
        return Unit(f(self, fo), _dim=dim, _epsilon=e)
    
    __call__ = __mul__
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        return self.__mul__(other, float.__truediv__, k=-1)

    def __floordiv__(self, other):
        return self.__mul__(other, float.__floordiv__, k=-1)
    
    def __pow__(self, exp):
        return Unit(
            float(self) ** exp,
            _dim = tuple(intify(v*exp) for v in self.dim),
            _epsilon = self.epsilon * abs(exp),
        )

    def __rtruediv__(self, other):
        return other * self ** -1
    
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
            op(float(self), other),
            _dim = self.dim,
            _delta = op(float(self.delta), odelta)
        )
    
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

class BaseUnit(Unit):
    __slots__ = Unit.__slots__ + ['symbols']
    
    def __new__(cls, value, *symbols, m=None, **kw):
        self = Unit.__new__(cls, value, **kw)
        self.symbols = symbols
        
        if m is not None:
            self.displayMeasures[self.dim] = (
                m, self if symbols else None)
        return self
    