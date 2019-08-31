"""Noether: International System of Units dimensionality object"""

import operator

from .scale import numberString, superscript
from .matrix import Matrix
#from .dimension import Dimension : Import loop

__all__ = 'Unit BaseUnit Dimension'.split()

class UnitMeta(type):
    """Metaclass of shared Unit properties"""
    def _dU_get(cls):
        return list(cls._displayUnits.values())

    def _dU_set(cls, bases):
        cls._displayUnits.clear()
        if isinstance(bases, dict):
            bases = bases.values()
        
        for unit in bases:
            cls._displayUnits[unit.dim] = unit

    def _dU_del(cls):
        cls._displayUnits.clear()
    
    def display(cls, unit):
        cls._displayUnits[unit.dim] = unit

    displayUnits = property(_dU_get, _dU_set, _dU_del)


class Unit(float, metaclass=UnitMeta):

    precision = 3
    showUnits = True
    showDimension = True
    openLinear = False
    unicodeExponent = True

    __slots__ = "dim _delta _epsilon".split()

    def __new__(cls, value=1, **kw):
        self = float.__new__(cls, value)

        if isinstance(value, Unit):
            dim, delta, eps = value.dim, value._delta, value._epsilon
        else:
            dim, delta, eps = None, None, None

        self.dim = Dimension(kw.get("_dim", dim))
        self._delta = kw.get("_delta", delta)
        self._epsilon = kw.get("_epsilon", eps)

        return self

    # Delta / epsilon (absolute / relative uncertainties)

    def _d_get(self):
        if self._delta is not None:
            return self._delta
        e, f = self._epsilon or 0, float(self)
        if e == 0 or f == 0:
            return 0
        else:
            return abs(e * f)

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
            return abs(d / f)

    def _e_set(self, e):
        self._epsilon = abs(e)
        self._delta = None

    epsilon = property(_e_get, _e_set, lambda s: s._e_set(0))

    # This class-shared variable is used for display units
    # {dim: Unit}
    _baseDisplayUnits = {}
    _displayUnits = {}

    @property
    def displayUnit(self):
        return self._displayUnits.get(
            self.dim, self._baseDisplayUnits.get(self.dim, None))

    @property
    def symbol(self):
        if self.displayUnit:
            return self.displayUnit.symbols[0]

    def value(self):
        '''Returns the number(s) without dimension.'''
        return Unit(float(self), _delta=self._delta, _epsilon=self._epsilon)

    def numberString(self, useDisplayUnit=False):
        display = self
        if useDisplayUnit and self.displayUnit:
            display /= self.displayUnit

        useParens = bool(self.symbol)
        return numberString(
            float(display),
            display.delta,
            useParens,
            self.precision,
            self.unicodeExponent,
        )

    def __str__(self):
        sNum = self.numberString(useDisplayUnit=True)

        if not self.showUnits:
            return sNum.strip()

        if sNum == "-1":
            sNum = "-"

        sNum += self.symbol or self.dim.asFundamentalUnits()

        return sNum + self._strDim()

    def __repr__(self):
        return str(self)
    
    def _strDim(self):
        if self.showDimension and self.dim.names:
            return " <{}>".format(', '.join(self.dim.names))
        else:
            return ""

    # Dimension-changing operators

    @property
    def invUnit(self):
        return Unit(tuple(-i for i in self.dim), _factor=float(self))

    @property
    def inv(self):
        return 1 / self

    def __mul__(self, other, f=operator.mul):
        if other is 1:
            return self

        if isinstance(other, Dimension):
            return f(self.dim, other)
        if isinstance(other, Unit):
            dim = f(self.dim, other.dim)
            e = self.epsilon + other.epsilon
        else:
            dim = self.dim
            e = self.epsilon

        return Unit(f(float(self), float(other)), _dim=dim, _epsilon=e)

    __call__ = __mul__
    __rmul__ = __mul__
    __truediv__ = lambda s, o: s.__mul__(o, operator.truediv)
    __floordiv__ = lambda s, o: s.__mul__(o, operator.floordiv)

    def __pow__(self, exp):
        return Unit(float(self)**exp,
                    _dim=self.dim**exp,
                    _epsilon=self.epsilon * abs(exp))

    def __rtruediv__(self, other):
        return other * self**-1

    # Linear operations

    __neg__ = lambda s: s * -1

    def __cmp(self, other):
        # Linear helper
        if not self.openLinear:
            if isinstance(other, Unit) and self.dim != other.dim:
                raise ValueError("Inequal units {} and {}.".format(
                    self.dim, other.dim))

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
        if isinstance(other, Dimension):
            return other._checkType(self)

        self.__cmp(other)
        odelta = other.delta if isinstance(other, Unit) else 0
        return Unit(
            op(float(self), float(other)),
            _dim=self.dim,
            _delta=op(float(self.delta), odelta),
        )

    def __sub__(self, other):
        return self.__add__(other, operator.sub)

    __radd__ = __add__
    __rsub__ = __sub__

    # comparison operators require range-checking

    def __eq__(self, other):
        if isinstance(other, Unit):
            if other.dim != self.dim:
                return False
            sl, su, ol, ou = self.__cmp(other)
            return ((sl <= ol <= su) or (sl <= ou <= su) or (ol <= sl <= ou)
                    or (ol <= su <= ou))

    def __ne__(self, other):
        sl, su, ol, ou = self.__cmp(other)
        return sl <= ou or ol <= su

    # __lt__ = lambda s, o: s.__cmp(o, operator.lt)
    # __le__ = lambda s, o: s.__cmp(o, operator.le)
    # __ge__ = lambda s, o: s.__cmp(o, operator.ge)
    # __gt__ = lambda s, o: s.__cmp(o, operator.gt)

    def __hash__(self):
        '''Not useful for direct equality comparison.'''
        return hash((float(self), self.dim))

    # Matrix operators

    def __and__(self, other):
        return Matrix(self) & other

    def __rand__(self, other):
        return other & Matrix(self)

    def __or__(self, other):
        return Matrix(self) | other

    def __ror__(self, other):
        return other | Matrix(self)


class BaseUnit(Unit):
    __slots__ = Unit.__slots__ + ["symbols", "names"]

    def __new__(cls, value, *a, symbols=None, names=None, isDisplay=False, **kw):
        if isinstance(value, Dimension):
            kw['_dim'] = value
            value = 1
        self = Unit.__new__(cls, value, **kw)
        self.symbols = symbols or tuple()
        self.symbols += a
        self.names = names or tuple()

        if symbols and isDisplay:
            self._baseDisplayUnits[self.dim] = self
        return self
    
    def __repr__(self):
        return (self.names + self.symbols + ('<unnamed unit>', ))[0] + self._strDim()

# Avoid name-mangling

from .dimension import Dimension
