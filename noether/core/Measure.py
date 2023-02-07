__all__ = ('Measure', )

from dataclasses import dataclass
from functools import total_ordering
import operator
from sys import version_info
from typing import Optional, TypeVar, ClassVar, Generic, TYPE_CHECKING
from numbers import Real

from noether.helpers import removeprefix

from ..errors import NoetherError, DimensionError
from ..config import Config, conf
from ..display import canonical_number
from .Dimension import Dimension, dimensionless
from .MeasureInfo import MeasureInfo

if TYPE_CHECKING:
    from .Unit import Unit
    from .MeasureRelative import MeasureRelative


OPENLINEAR = Config.register("measure_ignore_dimension", False, """\
Allow any addition, even between incompatible units
(eg metre and second)""")

BARENUMBER = Config.register("measure_barenumber", False, """\
Allow addition and subtraction of bare numbers to units""")

UNCERTAINTY_OVERLAP = Config.register("uncertainty_compare_range_overlap", False, """\
When comparing a Measure, compare on the uncertainty.
For == this means 'do the ranges overlap';
for < it means 'do the ranges not overlap'.""")

UNCERTAINTY_SHORTHAND = Config.register("uncertainty_display_shorthand", False, """\
Display e.g. 0.15(2) instead of 0.15 ± 0.02.""")

T = TypeVar('T', int, float, Real)  # typing of Measure


@dataclass(
    frozen=True,
    init=False,
    **(dict(slots=True) if version_info.minor >= 10 else dict()),
)
@total_ordering
class Measure(Generic[T]):
    '''
    A measurement, with Dimension and optional uncertainty.
    '''
    value: T
    stddev: Optional[T] = None
    dim: Dimension

    def __init__(
        self,
        value: "Measure[T] | T" = 1,
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

    info_handlers: ClassVar[list[type[MeasureInfo]]] = list()

    @classmethod
    def Info(cls, handler: type[MeasureInfo]):
        '''Wrapper for classes which implement MeasureInfo interface.'''
        if not issubclass(handler, MeasureInfo):
            raise TypeError(
                'Measure information handlers should derive from MeasureInfo.')
        if not handler.__name__.startswith('info_'):
            raise TypeError(
                'MeasureInfo classes must be prefixed with `info_`.')

        cls.info_handlers.append(handler)

        Config.register(handler.__name__,
                        handler.enabled_by_default,
                        handler.__doc__)

        return handler

    # |~~\ '      |
    # |   ||(~|~~\|/~~|\  /
    # |__/ |_)|__/|\__| \/
    #         |        _/

    def _info(self):
        for handler in self.info_handlers:
            if conf.get(handler.__name__) and handler.should_display(self):
                for i in handler.info(self):
                    yield i, handler.style

    def display_unit(self):
        from .DisplaySet import display
        units = display.units.get(self.dim, [])
        if units:
            return units[-1]

    def unit_to_display(self):
        from .DisplaySet import display  # noqa

        unit = self.dim.display(
            display_function=lambda x: display.dimension_symbol[x],
            drop_multiplication_signs=True,
        )

        return removeprefix(unit, '1 ')  # avoid "2  1 / m"

    def __repr__(self):
        if conf.get('display_repr_code'):
            return self.repr_code()
        return self.__noether__()

    def repr_code(self):
        chunks = [repr(self.value)]
        if self.stddev is not None:
            chunks.append(repr(self.stddev))
        if self.dim:
            chunks.append('dim=' + self.dim.repr_code())

        return 'Measure({})'.format(', '.join(chunks))

    @staticmethod
    def repr_measure(measure: 'Measure'):
        # Fallback if no unit found
        n = canonical_number(measure.value, measure.stddev,
                             conf.get(UNCERTAINTY_SHORTHAND))
        s = measure.unit_to_display()
        return f'{n} {s}'

    def _display_element(self):
        return (self.display_unit() or self).repr_measure(self)

    def __noether__(self):
        info = ', '.join(i for i, _ in self._info())
        if info:
            info = '  # ' + info
        return self._display_element() + info

    def __rich__(self):
        info = ', '.join(f'[{style}]{i}[/]' for i, style in self._info())
        if info:
            info = '  [green italic]#[/] ' + info
        return self._display_element() + info

    @staticmethod
    def str_measure(measure: 'Measure'):
        # Fallback if no unit found
        n = canonical_number(measure.value, measure.stddev,
                             conf.get(UNCERTAINTY_SHORTHAND))
        s = measure.unit_to_display()
        return f'{n} {s}'

    def __str__(self):
        return (self.display_unit() or self).str_measure(self)

    #  /~~\                   |     '
    # |  __/~//~\|/~\ /~\ /~/~|~|/~\|/~~
    #  \__/\/_\_/|   |   |\/_ | |   |\__

    def __geo(
        self,
        other: 'Measure[T] | Real',
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

    def __lin_cmp(self, other, operation: str):
        if conf.get(OPENLINEAR):
            return

        if isinstance(other, Measure):
            if self.dim != other.dim:
                raise DimensionError(
                    self.dim, other.dim,
                    f"To enable {operation} on mismatched dimensions enable conf.{OPENLINEAR}.")

        elif not conf.get(BARENUMBER):
            raise NoetherError(
                "A measure may not linearly operate on a number."
                f" Enable conf.{BARENUMBER} to suppress this.")

    def __lin(self, other: 'Measure[T] | Dimension | Real', op):
        self.__lin_cmp(
            other, 'addition' if op == operator.add else 'subtraction')

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
            if other.dim != self.dim and not conf.get(OPENLINEAR):
                return False
            if conf.get(UNCERTAINTY_OVERLAP):
                s_min, s_max = self.bounds
                o_min, o_max = other.bounds
                return ((s_min <= o_min <= s_max) or
                        (s_min <= o_max <= s_max) or
                        (o_min <= s_min <= o_max) or
                        (o_min <= s_max <= o_max))
            return self.value == other.value

    def __lt__(self, other):
        self.__lin_cmp(other, 'comparison')
        if isinstance(other, Measure):
            if conf.get(UNCERTAINTY_OVERLAP):
                s_min, s_max = self.bounds
                o_min, o_max = other.bounds
                return s_max < o_min
            return self.value < other.value

    #  /~~       |               |~~\ '      |
    # |  |   |(~~|~/~\|/~\ /~\   |   ||(~|~~\|/~~|\  /
    #  \__\_/|_) | \_/|   |   |  |__/ |_)|__/|\__| \/
    #                                    |        _/

    def __matmul__(self, unit: 'Unit'):
        from .Unit import Unit

        if not isinstance(unit, Unit):
            raise TypeError('Can only use @ (display relative to) on a Unit.')

        # HACK
        # We are intentionally deferring dimension checks.
        # This is because @ binds more tightly than &, * and /,
        # and so therefore until displayed we will
        # override these such that eg     a  @  b  /  c
        #               which binds as   (a  @  b) /  c
        # effortlessly becomes equiv to   a  @ (b  /  c)

        return MeasureRelative(self, unit)

    def __and__(self, unit: 'Unit'):
        from .units.ChainedUnit import ChainedUnit
        return ChainedUnit(self, unit)


# Avoid import loops
from .MeasureRelative import MeasureRelative  # noqa
