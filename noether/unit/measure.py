"""Noether: International System of Units dimensionality object"""

import operator

from .scale import numberString
# For matrix convenience
from ..matrix import Matrix
#from .dimension import Dimension : Import loop

__all__ = 'Measure Unit Dimension'.split()

class MeasureMeta(type):
    """Metaclass of shared Measure properties"""
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


class Measure(float, metaclass=MeasureMeta):
    # TODO: allow for int Measures with metaclasses

    precision = 3
    showUnits = True
    showDimension = True
    openLinear = False
    unicodeExponent = True

    __slots__ = "dim _stddev".split()

    def __new__(cls, value=1, stddev=None, dim=None):
        '''
        Extension to float with a dimension and standard deviation.

        Will propagate properties via standard operations, but will act
        like a float (and disregard properties) to functions designed
        to operate on numerics. Ensure Measure-aware functions are used
        if required.
        '''
        self = float.__new__(cls, value)

        if isinstance(value, Measure):
            self.dim = value.dim
            self._stddev = value._stddev
        else:
            self.dim = Dimension()
            self._stddev = 0

        if dim is not None:
            self.dim = Dimension(dim)
        if stddev is not None:
            self.stddev = stddev

        return self

    # Standard deviation

    def _stddev_set(self, v):
        self._stddev = abs(v)

    stddev = property(lambda s: s._stddev, _stddev_set, lambda s: s._stddev_set(0))
    delta = stddev

    def _stdratio_set(self, v):
        self.stddev = v * float(self)
    stddevratio = property(
        lambda s: abs(s._stddev / float(s)) if float(s) else 0,
        _stdratio_set,
        lambda s: s._stddev_set(0))
    epsilon = stddevratio

    def _variance_set(self, v):
        self.stddev = v ** 2
    variance = property(
        lambda s: s._stddev ** 0.5,
        _variance_set,
        lambda s: s._stddev_set(0)
    )

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
        return Measure(self, dim=Dimension())

    def numberString(self, useDisplayUnit=False):
        if useDisplayUnit and self.displayUnit:
            display /= self.displayUnit

        useParens = bool(self.symbol)
        return numberString(
            float(self),
            self.stddev,
            useParens,
            self.precision,
            self.unicodeExponent,
        )

    def __str__(self):
        sNum = self.numberString(useDisplayUnit=True)

        if not self.showUnits:
            return sNum.strip()

        sNum += self.symbol or self.dim.as_fundamental(as_units=True)

        return sNum + self._opt_dimension_name()

    def __format__(self, spec):
        return float.__format__(self, spec) + self.dim.as_fundamental(as_units=True)

    def __repr__(self):
        return str(self)
    
    def _opt_dimension_name(self):
        if self.showDimension and self.dim.names:
            return " <{}>".format(', '.join(self.dim.names))
        else:
            return ""

    # Dimension-changing operators

    @property
    def inv(self):
        return 1 / self

    def __geometric(self, other, op=operator.mul):

        new = Measure(
            op(float(self), float(other)),
            dim=self.dim,
            stddev=self.stddev
        )

        if isinstance(other, Dimension):
            raise TypeError('Unclear result of operator on Dimension and Measure. Use Measure.dim, or Measure(dim).')
        elif isinstance(other, Measure):
            new.dim = op(self.dim, other.dim)
            new.epsilon = (self.epsilon**2 + other.epsilon**2) ** 0.5
        else:
            new.epsilon = self.epsilon

        return new
    
    __rmul__ = __mul__ = lambda s, o: s.__geometric(o, operator.mul)
    __truediv__ = lambda s, o: s.__geometric(o, operator.truediv)
    __floordiv__ = lambda s, o: s.__geometric(o, operator.floordiv)

    def __call__(self, value, stddev=None):
        if stddev and not isinstance(value, Measure):
            value = Measure(value, stddev)
        return self * value

    def __pow__(self, exp):
        new = Measure(float(self)**exp, dim=self.dim**exp)
        new.epsilon = self.epsilon * exp
        return new

    def __rtruediv__(self, other):
        return other * self**-1

    # Linear operations

    __neg__ = lambda s: s * -1

    def __linear_compare(self, other):
        if not self.openLinear:
            if isinstance(other, Measure) and self.dim != other.dim:
                raise ValueError("Incompatible dimensions {} and {}.".format(
                    self.dim, other.dim))

        # Return limits of uncertainty
        # TODO: Extract this into a separate Range object - this is not standard deviation
        sl = float(self) - self.delta
        su = float(self) + self.delta
        if isinstance(other, Measure):
            ol = float(other) - other.delta
            ou = float(other) + other.delta
        else:
            ol, ou = other, other
        return sl, su, ol, ou

    def __linear(self, other, op=operator.add):
        if isinstance(other, Dimension):
            return other._checkType(self)

        self.__linear_compare(other)
        stddev = self.stddev
        if isinstance(other, Measure):
            stddev = (stddev**2 + other.stddev**2) ** 0.5
        return Measure(
            op(float(self), float(other)),
            dim=self.dim,
            stddev=stddev
        )
    
    __add__ = __radd__ = lambda s, o: s.__linear(o, operator.add)
    __sub__ = __rsub__ = lambda s, o: s.__linear(o, operator.sub)

    # comparison operators require range-checking

    def __eq__(self, other):
        if isinstance(other, Measure):
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


class Unit(Measure):
    __slots__ = Measure.__slots__ + ["symbols", "names"]

    def __new__(cls, value, *a, symbols=None, names=None, isDisplay=False, **kw):
        if isinstance(value, Dimension):
            kw['dim'] = value
            value = 1
        self = Measure.__new__(cls, value, **kw)
        self.symbols = symbols or tuple()
        self.symbols += a
        self.names = names or tuple()

        if symbols and isDisplay:
            self._baseDisplayUnits[self.dim] = self
        return self
    
    def __repr__(self):
        if self.names:
            return self.names[0] + self._opt_dimension_name()
        elif self.symbols:
            return self.symbols[0] + self._opt_dimension_name()
        else:
            return Measure.__repr__(self)

# Avoid name-mangling

from .dimension import Dimension
