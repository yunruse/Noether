__all__ = ('Measure', )

from typing import Callable, Optional, TypeVar, ClassVar, Generic, TYPE_CHECKING
from dataclasses import dataclass
from functools import total_ordering
import operator
from sys import version_info
from datetime import date, datetime, timedelta

from ..helpers import MeasureValue
from ..errors import NoetherError, DimensionError
from ..config import Config, conf
from ..display import DISPLAY_REPR_CODE

from .Prefix import Prefix
from .Dimension import Dimension, dimensionless
from .MeasureInfo import MeasureInfo

if TYPE_CHECKING:
    from .Unit import Unit
    from .UnitSet import UnitSet
    from .MeasureRelative import MeasureRelative

Time = date | datetime | timedelta
T = TypeVar('T', int, MeasureValue)


USE_DISPLAY_UNIT = Config.register(
    "measure_use_display_unit", False,
    "In situations where a unit is not explicitly provided, such as"
    " adding a float, converting to int, or rounding,"
    " make use of the current display unit rather than returning an error.")

# USE_OTHER_UNIT = Config.register(
#     "measure_use_other_unit", False,
#     "In situations where a unit is not explicitly provided, such as"
#     " meter + 5, use the other unit provided in the calculation"
# )
# TODO: is the above actually technically feasible?

UNCERTAINTY_SHORTHAND = Config.register(
    "measure_uncertainty_shorthand", False,
    "Use shorthand for uncertainty, for example 0.15(2) rather than 0.15 ± 0.02"
)

SI_EQUALITY = Config.register(
    "measure_si_equality", False,
    "If enabled, equality is true even between incompatible units (eg meter and kilogram) based on their SI value. Cf .openlinear"
)


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
    _value: T
    stddev: Optional[T] = None
    dim: Dimension

    def __init__(
        self,
        value: "Measure[T] | T | timedelta" = 1,
        stddev: Optional[T] = None,
        dim: Optional[Dimension] = None,
    ):
        if isinstance(value, timedelta):
            value = self.from_timedelta(value)

        def set(x, v):
            # bypass Frozen
            object.__setattr__(self, x, v)

        if isinstance(value, Measure):
            set('_value', value._value)
            set('stddev', value.stddev)
            set('dim', value.dim)
        else:
            set('_value', value)
            set('stddev', None)
            set('dim', dimensionless)

        if stddev is not None:
            set('stddev', stddev)
        if dim is not None:
            set('dim', dim)

        if not isinstance(self._value, MeasureValue):
            raise TypeError('value must be a real number, not a'
                            f' {type(self._value).__name__}')

        if self.stddev is not None:
            if not isinstance(self.stddev, MeasureValue):
                raise TypeError('stddev must be a real number, not a'
                                f' {type(self.stddev).__name__}')

    def cast(self, to: type):
        return Measure(
            to(self._value),
            to(self.stddev),
            self.dim)

    @property
    def epsilon(self):
        if self.stddev is None or not self._value:
            return None
        return self.stddev / self._value

    # |\  |              |
    # | \ ||   ||/~\ /~\ |~~\/~/|/~\
    # |  \| \_/||   |   ||__/\/_|

    @property
    def value(self):
        # TODO: this is used in a whole bunch of places
        # but because it relies on the underlying SI value it is rather hacky.
        # Per #84 this should be tightened up
        return self._value

    def __bool__(self):
        return bool(self._value)

    def _casting_value(self) -> T:
        "Value to use for `int`, `float`, `round`, `self.real`, and so on."
        if not self.dim:
            return self._value

        du = self.display_unit()

        if conf.get(USE_DISPLAY_UNIT):
            from .units.LinearUnit import LinearUnit
            # e.g. 'lb & st' - which one do we use?
            if isinstance(du, LinearUnit):
                raise NoetherError(
                    f"Even with {USE_DISPLAY_UNIT}, {du} is ambiguous for this kind of operation."
                    " Try using `measure @ unit` or `measure / unit`."
                )
            return self._value / du._value

        raise NoetherError(
            f"Without a unit this operation is ambiguous. Try using `measure @ unit`, `measure / unit`"
            f" or enabling {USE_DISPLAY_UNIT} if you are ok with a little ambiguity.")

    def __float__(self):
        return float(self._casting_value())

    def __int__(self):
        return int(self._casting_value())

    def __round__(self, ndigits: Optional[int] = None):
        return round(self._casting_value(), ndigits)

    @property
    def real(self):
        return self._casting_value()

    @property
    def imag(self):
        return 0

    @property
    def numerator(self):
        return self._casting_value().numerator

    @property
    def denominator(self):
        return self._casting_value().denominator

    @property
    def conjugate(self):
        return self._casting_value().conjugate()

    @property
    def as_integer_ratio(self):
        return self._casting_value().as_integer_ratio()

    info_handlers: ClassVar[list[type[MeasureInfo]]] = list()

    @classmethod
    def from_timedelta(cls, dt: timedelta):
        from ..catalogue import second
        return second * dt.total_seconds()

    def to_timedelta(self):
        from ..catalogue import second, time
        DimensionError.check(self.dim, time)
        return timedelta(seconds=float(self/second))

    # |~~\ '      |
    # |   ||(~|~~\|/~~|\  /
    # |__/ |_)|__/|\__| \/
    #         |        _/

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

    def _info(self):
        for handler in self.info_handlers:
            if conf.get(handler.__name__) and handler.should_display(self):
                for i in handler.info(self):
                    yield i, handler.style

    def display_unit(self) -> 'Unit':
        "The unit that should be used to display this object."
        from ._DisplayHandler import display
        return display.dimension_unit(self.dim)

    def __repr__(self):
        # TODO: this really should actually be code a user could make use of
        # with any niceties shoved into the 'comment' ...
        if conf.get(DISPLAY_REPR_CODE):
            return self._repr_code()
        return self.__noether__()

    def _repr_code(self):
        chunks = [repr(self._value)]
        if self.stddev is not None:
            chunks.append(repr(self.stddev))
        if self.dim:
            chunks.append('dim=' + self.dim._repr_code())

        return 'Measure({})'.format(', '.join(chunks))

    def __str__(self):
        return self.display_unit()._repr_measure(self)

    def __noether__(self):
        info = ', '.join(i for i, _ in self._info())
        if info:
            info = '  # ' + info
        return str(self).strip() + info

    def __rich__(self):
        info = ', '.join(f'[{style}]{i}[/]' for i, style in self._info())
        if info:
            info = '  [green italic]#[/] ' + info
        return str(self).strip() + info

    #  /~~\                   |     '
    # |  __/~//~\|/~\ /~\ /~/~|~|/~\|/~~
    #  \__/\/_\_/|   |   |\/_ | |   |\__

    def __geo(
        self,
        other: 'Measure[T] | MeasureValue | timedelta',
        op=operator.mul
    ) -> 'Measure':
        if isinstance(other, timedelta):
            return op(self, self.from_timedelta(other))

        value = self._value
        stddev = None
        dim = self.dim

        if isinstance(other, Prefix):
            other = other.value

        if isinstance(other, Measure):
            value = op(self._value, other._value)
            dim = op(self.dim, other.dim)
            if self.epsilon is not None or other.epsilon is not None:
                se = self.epsilon or 0
                oe = other.epsilon or 0
                stddev = value * (se**2 + oe**2)**0.5
        else:
            value = op(self._value, other)

        return Measure(value, stddev, dim)

    def __mul__(self, other): return self.__geo(other)
    def __rmul__(self, other): return self.__geo(other)
    def __truediv__(self, other): return self.__geo(other, operator.truediv)
    def __floordiv__(self, other): return self.__geo(other, operator.floordiv)

    def __rtruediv__(self, other): return other * self**-1

    def __call__(self, value: MeasureValue, stddev: Optional[MeasureValue] = None):
        return self * Measure(value, stddev)

    def __pow__(self, exp):
        return Measure(
            self._value ** exp,
            (None if self.epsilon is None
                else (self._value ** exp) * self.epsilon * exp),
            self.dim ** exp,
        )

    # |  '
    # |  ||/~\ /~//~~||/~\
    # |__||   |\/_\__||

    def __neg__(self): return self * -1
    def __pos__(self): return self

    def __abs__(self):
        return self if self._value > 0 else -self  # type: ignore

    def __linear_value(self, other) -> 'MeasureValue':
        if isinstance(other, Measure):
            DimensionError.check(self.dim, other.dim)
            return other._value

        if conf.get(USE_DISPLAY_UNIT):
            return other * self.display_unit()

        if self.dim and not conf.get(USE_DISPLAY_UNIT):
            raise NoetherError(
                f"{other} of what? No unit was provided."
                f" Consider enabling conf.{USE_DISPLAY_UNIT}"
                # f" or conf.{USE_OTHER_UNIT}"
            )
        return other

    def __lin(self, other: 'Measure[T] | Dimension | MeasureValue | Time', op: Callable, reverse=False):
        if isinstance(other, Time):
            if reverse:
                return op(other, self.to_timedelta())
            else:
                return op(self.to_timedelta(), other)

        value = self._value
        stddev = self.stddev
        dim = self.dim

        if reverse:
            value = op(self.__linear_value(other), self._value)
        else:
            value = op(self._value, self.__linear_value(other))

        if isinstance(other, Measure) and self.stddev and other.stddev:
            ss = 0 if stddev is None else stddev
            so = 0 if other.stddev is None else other.stddev
            stddev = (ss**2 + so**2) ** 0.5

        return Measure(value, stddev, dim)

    def __add__(self, other): return self.__lin(other, operator.add)
    def __radd__(self, other): return self.__lin(other, operator.add)
    def __sub__(self, other): return self.__lin(other, operator.sub)

    def __rsub__(self, other):
        return self.__lin(other, operator.sub, reverse=True)

    def __mod__(self, other): return self.__lin(other, operator.mod)

    # Equality and ordering

    @staticmethod
    def _extract_dim(v: 'Measure | MeasureValue') -> Dimension:
        return v.dim if isinstance(v, Measure) else Dimension()

    @staticmethod
    def _extract_value(v: 'Measure[T] | T') -> T:
        return v._value if isinstance(v, Measure) else v

    def __eq__(self, other):
        if self._extract_dim(other) != self.dim and not conf.get(SI_EQUALITY):
            return False
        return self._value == self.__linear_value(other)

    def __lt__(self, other):
        return self._value < self.__linear_value(other)

    #  /~~       |               |~~\ '      |
    # |  |   |(~~|~/~\|/~\ /~\   |   ||(~|~~\|/~~|\  /
    #  \__\_/|_) | \_/|   |   |  |__/ |_)|__/|\__| \/
    #                                    |        _/

    def __matmul__(self, display_with: 'Unit | UnitSet'):
        from .Unit import Unit
        from .UnitSet import UnitSet

        if isinstance(display_with, UnitSet):
            unit = display_with.unit_for_dimension(self.dim)
            if unit is None:
                return self
            return self @ unit

        if not isinstance(display_with, Unit):
            raise TypeError('Can only use @ (display relative to) on a Unit.')

        # HACK
        # We are intentionally deferring dimension checks.
        # This is because @ binds more tightly than &, * and /,
        # and so therefore until displayed we will
        # override these such that eg     a  @  b  /  c
        #               which binds as   (a  @  b) /  c
        # effortlessly becomes equiv to   a  @ (b  /  c)

        return MeasureRelative(self, display_with)

    def __rmatmul__(self, display_this: 'Measure | timedelta'):
        if isinstance(display_this, timedelta):
            display_this = self.from_timedelta(display_this)
        return Measure(display_this) @ self


# Avoid import loops
from .MeasureRelative import MeasureRelative  # noqa
