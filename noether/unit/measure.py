"""Noether: International System of Units dimensionality object"""

import operator

from .display import number_string
# For matrix convenience
from ..matrix import Matrix
#from .dimension import Dimension : Import loop

__all__ = 'Measure Unit Dimension'.split()

class MeasureMeta(type):
    """Metaclass of class-shared properties for display."""
    def _dU_get(cls):
        return list(cls._display_units.values())

    def _dU_set(cls, bases):
        cls.display()
        cls.display(*bases)

    def _dU_del(cls):
        cls._display_units.clear()
    
    def display(cls, *units):
        '''Registers unit for display, or, if given none, reverts all.'''
        if units:
            for u in units:
                if not isinstance(u, Unit):
                    u = u / float(u)
                cls._display_units[u.dim] = u
        else:
            cls._display_units.clear()

    display_units = property(_dU_get, _dU_set, _dU_del)


class Measure(float, metaclass=MeasureMeta):
    """
    A physical measurement.
    Represented by a float with dimension and uncertainty.
    """

    # TODO: allow for int Measures..?

    precision = 3
    show_units = True
    show_dimension = True
    open_linear = False
    unicode_exponent = True

    # These class-shared variable are used for display units
    # {dim: Unit}
    _base_display_units = {}
    _display_units = {}

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

    # Display

    @property
    def display_unit(self):
        return self._display_units.get(
            self.dim, self._base_display_units.get(self.dim, None))

    def as_fundamental(self):
        return self.dim.as_fundamental(as_units=True)

    @property
    def symbol(self):
        if self.display_unit:
            if isinstance(self, Unit):
                return self.display_unit.symbols[0]
        return self.as_fundamental()

    def value(self):
        '''Returns the number(s) without dimension.'''
        return Measure(self, dim=Dimension())

    def number_string(self, use_display_unit=False):
        display = self
        if use_display_unit and self.display_unit:
            display /= self.display_unit

        as_unit = bool(self.symbol)
        return number_string(
            float(display), display.stddev,
            self.precision, as_unit,
            self.unicode_exponent
        )
    
    def __str__(self):
        s = self.number_string(use_display_unit=True)
        if self.show_units:
            s += self.symbol + self._opt_dimension_name()
        return s

    def __format__(self, spec):
        return number_string(
            float(self), self.stddev,
            unicode_exponent=self.unicode_exponent,
            formatter=lambda x: format(x, spec)
        ) + self.symbol

    def __repr__(self):
        return str(self)
    
    def _opt_dimension_name(self):
        if self.show_dimension and self.dim.names:
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
        if not self.open_linear:
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
        if self.names:
            return self.names[0] + self._opt_dimension_name()
        elif self.symbols:
            return self.symbols[0] + self._opt_dimension_name()
        else:
            return Measure.__repr__(self)

# Avoid name-mangling

from .dimension import Dimension
