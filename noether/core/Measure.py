
from dataclasses import dataclass
from functools import total_ordering
import operator
from typing import Optional, TypeVar, Generic
from numbers import Real

from ..errors import DimensionError
from .config import Config, conf
from .display import plus_minus_symbol, NoetherRepr, uncertainty
from .Dimension import Dimension, dimensionless

Config.register("measure_openlinear", False, """\
Allow any addition, even between incompatible units
(eg metre and second)""")

Config.register("measure_barenumber", False, """\
Allow addition and subtraction of bare numbers to units""")

Config.register("measure_compare_uncertainty", False, """\
When comparing a Measure, compare on the uncertainty.
For == this means 'do the ranges overlap';
for < it means 'do the ranges not overlap'.""")

Config.register("measure_uncertainty_shorthand", False, """\
Display e.g. 0.15(2) instead of 0.15 ± 0.02.""")

T = TypeVar('T', int, float, Real)


@dataclass(
    frozen=True,
    init=False,
    slots=True,
)
@total_ordering
class Measure(NoetherRepr, Generic[T]):
    '''
    A measurement, with Dimension and optional uncertainty.
    '''

    value: T
    stddev: Optional[T] = None
    dim: Dimension

    def __init__(
        self,
        value: "Measure[T]" | T = 1,
        stddev: Optional[T] = None,
        dim: Optional[Dimension] = None,
    ):
        def set(x, v):
            # bypass Frozen
            object.__setattr__(self, x, v)

        if isinstance(value, Measure):
            set('value', value.value)
            set('stddev', value.stddev)
            set('dim', value.dim)
        else:
            set('value', value)
            set('stddev', None)
            set('dim', dimensionless)

        if stddev is not None:
            set('stddev', stddev)
        if dim is not None:
            set('dim', dim)

        if not isinstance(self.value, Real):
            raise TypeError('Value must be a real number, not a'
                            f' {type(self.value).__name__}')

        if self.stddev is not None:
            if not isinstance(self.stddev, Real):
                raise TypeError('stddev must be a real number, not a'
                                f' {type(self.stddev).__name__}')

    def cast(self, to: type):
        return Measure(
            to(self.value),
            to(self.stddev),
            self.dim)

    @property
    def epsilon(self):
        if self.stddev is None or not self.value:
            return None
        return self.stddev / self.value

    @property
    def bounds(self) -> tuple[T, T]:
        if self.stddev is None:
            return self.value, self.value
        return self.value - self.stddev, self.value + self.stddev  # type: ignore

    # |\  |              |
    # | \ ||   ||/~\ /~\ |~~\/~/|/~\
    # |  \| \_/||   |   ||__/\/_|

    def __float__(self): return float(self.value)
    def __int__(self): return int(self.value)
    def __bool__(self): return bool(self.value)

    @property
    def real(self): return self.value
    @property
    def imag(self): return 0
    @property
    def numerator(self): return self.value.numerator  # type: ignore
    @property
    def denominator(self): return self.value.denominator  # type: ignore
    @property
    def conjugate(self): return self.value.conjugate()  # type: ignore

    @property
    def as_integer_ratio(self):
        return self.value.as_integer_ratio()  # type: ignore

    # |~~\ '      |
    # |   ||(~|~~\|/~~|\  /
    # |__/ |_)|__/|\__| \/
    #         |        _/

    def __repr_code__(self):
        chunks = [repr(self.value)]
        if self.stddev is not None:
            chunks.append(repr(self.stddev))
        if self.dim:
            chunks.append(repr(self.dim))

        return 'Measure({})'.format(', '.join(chunks))

    def _symbol(self):
        from .DisplaySet import display  # noqa
        units = display.units.get(self.dim, [])
        if units:
            return units[-1].symbols[0]

    def canonical_value(self):
        if self.stddev is not None:
            if conf.get('measure_uncertainty_shorthand'):
                return uncertainty(self.value, self.stddev)
            else:
                pm = plus_minus_symbol()
                return f'{self.value} {pm} {self.stddev}'
        if isinstance(self.value, float) and self.value.is_integer():
            return repr(int(self.value))
        return repr(self.value)

    def __noether__(self):
        s = self._symbol()
        d = self.dim.canonical_name()
        v = self.canonical_value()
        return f'{v} {s} <{d}>'

    __str__ = __noether__

    def __rich__(self):
        s = self._symbol()
        d = self.dim.canonical_name()
        v = self.canonical_value()
        return f'{v} [red]{s}[/] <[grey italic]{d}[/]>'

    #  /~~\                   |     '
    # |  __/~//~\|/~\ /~\ /~/~|~|/~\|/~~
    #  \__/\/_\_/|   |   |\/_ | |   |\__

    def __geo(
        self,
        other: 'Measure[T] | Dimension | Real',
        op=operator.mul
    ) -> 'Measure':
        value = self.value
        stddev = None
        dim = self.dim

        if isinstance(other, Measure):
            value = op(self.value, other.value)
            dim = op(self.dim, other.dim)
            if self.epsilon is not None or other.epsilon is not None:
                se = self.epsilon or 0
                oe = other.epsilon or 0
                stddev = value * (se**2 + oe**2)**0.5
        elif isinstance(other, Dimension):
            dim = op(self.dim, other)
        else:
            value = op(self.value, other)

        return Measure(value, stddev, dim)

    def __mul__(self, other): return self.__geo(other)
    def __rmul__(self, other): return self.__geo(other)
    def __truediv__(self, other): return self.__geo(other, operator.truediv)
    def __floordiv__(self, other): return self.__geo(other, operator.floordiv)

    def __rtruediv__(self, other): return other * self**-1

    def __call__(self, value: Real, stddev: Optional[Real] = None):
        return self * Measure(value, stddev)

    def __pow__(self, exp):
        return Measure(
            self.value ** exp,
            (None if self.epsilon is None
                else (self.value ** exp) * self.epsilon * exp),
            self.dim ** exp,
        )

    # |  '
    # |  ||/~\ /~//~~||/~\
    # |__||   |\/_\__||

    def __neg__(self): return self * -1
    def __pos__(self): return self
    def __abs__(self): return self if self.value > 0 else -self  # type: ignore

    def __lin_cmp(self, other):
        if conf.get('measure_openlinear'):
            return

        if isinstance(other, Measure):
            if self.dim != other.dim:
                raise DimensionError(
                    f"{self.dim!r} and {other.dim!r}"
                    " are incompatible dimensions."
                    " Enable conf.measure_openlinear to suppress this.")

        elif not conf.get('measure_barenumber'):
            raise DimensionError(
                "A measure may not linearly operate on a number."
                " Enable conf.measure_barenumber to suppress this.")

    def __lin(self, other: 'Measure[T] | Dimension | Real', op=operator.add):
        self.__lin_cmp(other)

        value = self.value
        stddev = self.stddev
        dim = self.dim

        if isinstance(other, Dimension):
            pass
        elif isinstance(other, Measure):
            value = op(self.value, other.value)
            if self.stddev is None and other.stddev is None:
                stddev = None
            else:
                ss = 0 if stddev is None else stddev
                so = 0 if other.stddev is None else other.stddev
                stddev = (ss**2 + so**2) ** 0.5
        else:
            value = op(self.value, other)

        return Measure(value, stddev, dim)

    def __add__(self, other): return self.__lin(other, operator.add)
    def __radd__(self, other): return self.__lin(other, operator.add)
    def __sub__(self, other): return self.__lin(other, operator.sub)

    def __eq__(self, other):
        if isinstance(other, Measure):
            if other.dim != self.dim:
                return False
            if conf.get('measure_compare_uncertainty'):
                s_min, s_max = self.bounds
                o_min, o_max = other.bounds
                return ((s_min <= o_min <= s_max) or
                        (s_min <= o_max <= s_max) or
                        (o_min <= s_min <= o_max) or
                        (o_min <= s_max <= o_max))
            return self.value == other.value

    def __lt__(self, other):
        self.__lin_cmp(other)
        if isinstance(other, Measure):
            if conf.get('measure_compare_uncertainty'):
                s_min, s_max = self.bounds
                o_min, o_max = other.bounds
                return s_max < o_min
            return self.value < other.value

    # TODO: rest :)
