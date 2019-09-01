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

    __slots__ = "dim _delta".split()

    def __new__(cls, value=1, delta=None, dim=None):
        '''
        Extension to float with a Dimension and a uncertainty `delta`.

        Will propagate properties via standard operations, but will act
        like a float (and disregard properties) to functions designed
        to operate on numerics. Ensure Unit-aware functions are used
        if required.
        '''
        self = float.__new__(cls, value)

        if isinstance(value, Unit):
            self.dim = value.dim
            self._delta = value._delta
        else:
            self.dim = Dimension()
            self._delta = 0

        if dim is not None:
            self.dim = Dimension(dim)
        if delta is not None:
            self.delta = delta

        return self

    # Delta / epsilon (absolute / relative uncertainties)

    def _d_set(self, d):
        self._delta = abs(d)

    delta = property(lambda s: s._delta, _d_set, lambda s: s._d_set(0))

    def _e_set(self, e):
        self._delta = abs(e * float(self))

    epsilon = property(lambda s: abs(s._delta / float(s)), _e_set,
                       lambda s: s._e_set(0))

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
        return Unit(self, dim=Dimension())

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

    def __mul__(self, other, op=operator.mul, expOp=operator.add):

        new = Unit(
            op(float(self), float(other)),
            dim=self.dim,
            delta=self.delta
        )

        if isinstance(other, Dimension):
            raise TypeError('Unclear result of operator on Dimension and Unit. Use Unit.dim, or Unit(dim).')
        elif isinstance(other, Unit):
            new.dim = op(self.dim, other.dim)
            new.epsilon = expOp(self.epsilon, other.epsilon)
        else:
            new.epsilon = self.epsilon

        return new
    
    __rmul__ = __mul__
    __truediv__ = lambda s, o: s.__mul__(o, operator.truediv, operator.sub)
    __floordiv__ = lambda s, o: s.__mul__(o, operator.floordiv, operator.sub)

    def __call__(self, value, delta=None):
        if delta and not isinstance(value, Unit):
            value = Unit(value, delta)
        return self * value

    def __pow__(self, exp):
        new = Unit(float(self)**exp, dim=self.dim**exp)
        new.epsilon = self.epsilon * exp
        return new

    def __rtruediv__(self, other):
        return other * self**-1

    # Linear operations

    __neg__ = lambda s: s * -1

    def __linear_compare(self, other):
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

        self.__linear_compare(other)
        odelta = other.delta if isinstance(other, Unit) else 0
        return Unit(
            op(float(self), float(other)),
            dim=self.dim,
            delta=op(float(self.delta), odelta),
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
            kw['dim'] = value
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
