"""Noether: International System of Units dimensionality object"""

import operator

from .helpers import intify
from .scale import numberString, superscript
from .matrix import Matrix


class Dimension(tuple):
    fundamental = "Cd rad B A K m s mol Kg".split()
    N_DIMENSIONS = len(fundamental)

    def __new__(cls, name_or_tuple=None):
        if isinstance(name_or_tuple, tuple):
            val = name_or_tuple
        elif isinstance(name_or_tuple, str):
            val = cls._names.get(name_or_tuple)
        elif isinstance(name_or_tuple, int):
            val = tuple(name_or_tuple == i + 1 for i in range(cls.N_DIMENSIONS))
        else:
            val = tuple([0] * cls.N_DIMENSIONS)
        return tuple.__new__(Dimension, val)

    # Names: a dictionary of Dimension to Name
    _names = {}
    name = property(lambda s: s._names.get(s, None))

    def asFundamentalUnits(self):
        dims = []
        for sym, exp in zip(self.fundamental, self):
            if exp == 0:
                continue
            elif exp != 1:
                if Unit.unicodeExponent:
                    sym += str(exp).translate(superscript)
                else:
                    sym += "^" + str(exp)
            dims.append(sym)

        return "·".join(dims)

    __str__ = asFundamentalUnits

    def __repr__(self):
        return "Dimension({!r})".format(
            self._names.get(self, tuple(self) if self else None)
        )

    def __bool__(self):
        return not all(i == 0 for i in self)

    def _checkType(self, other):
        """Check and attempt to match other unit to Dimension"""
        if isinstance(other, (float, int)):
            return Dimension()
        if isinstance(other, Dimension):
            return other
        elif isinstance(other, Unit):
            return other.dim
        else:
            raise TypeError(
                "Cannot operate on Dimension with {}".format(type(other).__name__)
            )

    def __mul__(self, other):
        other = self._checkType(other)
        return Dimension(tuple(u + v for (u, v) in zip(self, other)))

    def __pow__(self, exp):
        if isinstance(exp, (int, float)):
            return Dimension(tuple(intify(v * exp) for v in self))
        else:
            raise TypeError("Cannot raise dimension to non-real exponent")

    def __truediv__(self, other):
        other = self._checkType(other)
        return Dimension(tuple(u - v for (u, v) in zip(self, other)))

    def __rtruediv__(self, exp):
        return self._checkType(exp) / self

    __floordiv__ = __truediv__
    __rfloordiv__ = __rtruediv__
    __rmul__ = __mul__
    __pos__ = __neg__ = lambda s: s

    def _checkLinear(self, other):
        other = self._checkType(other)
        if self == other:
            return self
        else:
            raise ValueError(
                "Cannot linearly operate on inequal dimensions {} and {}".format(
                    self, other
            ))

    __sub__ = __rsub__ = __add__ = __radd__ = _checkLinear


class UnitMeta(type):
    """Metaclass of shared Unit properties"""

    def _dU_get(cls):
        return list(cls._displayUnits.values())

    def _dU_set(cls, bases):
        cls._displayUnits.clear()
        if not hasattr(bases, "__iter__"):
            bases = [bases]
        for unit in bases:
            cls._displayUnits[unit.dim] = unit

    def _dU_del(cls):
        cls._displayUnits.clear()

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

    # Any units set as a measure (i.e. base SI units)
    # are stored here for display:
    # {dim: Unit}
    _baseDisplayUnits = {}
    _displayUnits = {}

    @property
    def displayUnit(self):
        return self._displayUnits.get(
            self.dim, self._baseDisplayUnits.get(self.dim, None)
        )

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

        if self.showDimension and self.dim.name:
            sNum += " ({})".format(self.dim.name)

        return sNum

    __repr__ = __str__

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
        return Unit(
            float(self) ** exp, _dim=self.dim ** exp, _epsilon=self.epsilon * abs(exp)
        )

    def __rtruediv__(self, other):
        return other * self ** -1

    # Linear operations

    __neg__ = lambda s: s * -1

    def __cmp(self, other):
        # Linear helper
        if not self.openLinear and isinstance(other, Unit) and self.dim != other.dim:
            raise ValueError("Inequal units {} and {}.".format(self.dim, other.dim))

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
        sl, su, ol, ou = self.__cmp(other)
        return (
            (sl <= ol <= su) or (sl <= ou <= su) or (ol <= sl <= ou) or (ol <= su <= ou)
        )

    def __ne__(self, other):
        sl, su, ol, ou = self.__cmp(other)
        return sl <= ou or ol <= su

    # __lt__ = lambda s, o: s.__cmp(o, operator.lt)
    # __le__ = lambda s, o: s.__cmp(o, operator.le)
    # __ge__ = lambda s, o: s.__cmp(o, operator.ge)
    # __gt__ = lambda s, o: s.__cmp(o, operator.gt)

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
    __slots__ = Unit.__slots__ + ["symbols"]

    def __new__(cls, value, *symbols, isDisplay=False, **kw):
        self = Unit.__new__(cls, value, **kw)
        self.symbols = symbols

        if symbols and isDisplay:
            self._baseDisplayUnits[self.dim] = self
        return self
