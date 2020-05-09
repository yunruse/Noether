"""Noether: International System of Units dimensionality object"""

import operator

from ..conf import conf

from ..display import number_string

from .dimension import Dimension

__all__ = ('Measure', )

# TODO: emit Warning (or else use display unit!) if adding bare number

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
        # TODO: desperately change display mechanism
        if units:
            for u in units:
                cls._display_units[u.dim] = u
        else:
            cls._display_units.clear()

    display_units = property(_dU_get, _dU_set, _dU_del)

conf.register(
    "measure_openlinear", bool, False,
    "Allow any addition, even between incompatible units (eg metre and second)"
)

conf.register(
    "measure_precision", int, 3,
    "The maximum amount of decimal places to display when using repr(Measure)."
)

conf.register(
    "unicode_exponent", bool, True,
    "Use Unicode superscripts instead of the ^ when displaying units."
)

conf.register("info_dimension", bool, True, """\
Show dimension name(s) for units and measures.""")

class Measure(float, metaclass=MeasureMeta):
    """
    A physical measurement.
    Represented by a float with dimension and uncertainty.
    """

    # TODO: allow for int Measures..?

    show_units = True
    show_dimension = True

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
            conf.measure_precision, as_unit,
            conf.unicode_exponent
        )
    
    def __str__(self):
        s = self.number_string(use_display_unit=True)
        if self.show_units:
            s += self.symbol

        opt = []
        if conf.info_dimension and self.dim.names:
            opt += self.dim.names

        if opt:
            s += f" <{', '.join(opt)}>"

        return s

    def __format__(self, spec):
        return number_string(
            float(self), self.stddev,
            unicode_exponent=conf.unicode_exponent,
            formatter=lambda x: format(x, spec)
        ) + self.symbol

    def __repr__(self):
        return str(self)

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
            raise TypeError('Ambiguous operation Dimension and Measure. Resolve with Dimension(measure) or Measure(dim).')
        elif isinstance(other, Measure):
            new.dim = op(self.dim, other.dim)
            new.epsilon = (self.epsilon**2 + other.epsilon**2) ** 0.5
        else:
            new.epsilon = self.epsilon

        return new
    
    # TODO: automatic conversion when units match certain relations (eg MeV, MeV/c, MeV/c^2)
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
        if not conf.measure_openlinear:
            if isinstance(other, Measure) and self.dim != other.dim:
                raise ValueError("Incompatible dimensions {} and {}.".format(
                    self.dim, other.dim))

        # Return limits of uncertainty
        # TODO: extract uncertainty behaviour into various Uncertain classes
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
            sl, su, ol, ou = self.__linear_compare(other)
            return ((sl <= ol <= su) or (sl <= ou <= su) or (ol <= sl <= ou)
                    or (ol <= su <= ou))

    def __ne__(self, other):
        sl, su, ol, ou = self.__linear_compare(other)
        return sl <= ou or ol <= su

    # __lt__ = lambda s, o: s.__cmp(o, operator.lt)
    # __le__ = lambda s, o: s.__cmp(o, operator.le)
    # __ge__ = lambda s, o: s.__cmp(o, operator.ge)
    # __gt__ = lambda s, o: s.__cmp(o, operator.gt)

    def __hash__(self):
        '''Not useful for direct equality comparison.'''
        return hash((float(self), self.dim))

    # Matrix operators for user convenience.
    # Import explicitly, as they are only used for user convenience;
    # otherwise numpy would be loaded, slowing down startup

    def __and__(self, other):
        from ..matrix import Matrix
        return Matrix(self) & other

    def __rand__(self, other):
        from ..matrix import Matrix
        return other & Matrix(self)

    def __or__(self, other):
        from ..matrix import Matrix
        return Matrix(self) | other

    def __ror__(self, other):
        from ..matrix import Matrix
        return other | Matrix(self)

    # TODO: have @ display in a unit, eg `x @ mile&inch`
