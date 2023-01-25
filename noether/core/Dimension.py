from dataclasses import dataclass
from fractions import Fraction
from numbers import Number
from typing import Callable

from ..helpers import ImmutableDict, reorder_dict_by_values
from ..errors import DimensionError


@dataclass(slots=True, frozen=True, order=True)
class DimInfo:
    order: float
    symbol: str


class Dimension(ImmutableDict):
    '''
    Dimension of a unit.

    Internally, a dict of names to Fractions.
    The dimension names are stored in _names,
    alongside their display order.
    '''

    # Class variable with display order
    _names: dict[str, DimInfo] = dict()

    # Instantiation

    @classmethod
    def new(
        cls,
        name: str,
        symbol: str,
        order: float = 0,
    ):
        '''
        Register a new base dimension and return its unit.
        '''
        cls._names[name] = DimInfo(order, symbol)
        reorder_dict_by_values(cls._names)
        return cls({name: Fraction(1)})

    def __init__(self, value=None, **kw):
        if value is None:
            value = dict()
        elif isinstance(value, Unit):
            value = value.dim
        if not isinstance(value, dict):
            raise TypeError(
                'Can only instantiate from a Dimension, Unit or Dict.')

        value.update(kw)

        for name, exp in value.copy().items():
            if not exp:
                del value[name]
            if name not in self._names:
                raise DimensionError(
                    f'Unknown dimension {name}')
        super().__init__(value)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    def is_fundamental(self):
        return self.values() == [1]

    def as_fundamental(
        self, /,
        display: Callable[[str], str] = lambda x: x
    ):
        if not self:
            return display('dimensionless')
        exponents = list(self.items())
        exponents.sort(key=lambda q: (q[1] < 0, self._names[q[0]].order))

        string = '1'
        for name, exp in exponents:
            symbol = '*'
            use_brackets = exp.denominator != 1
            if not use_brackets and exp < 0:
                symbol = '/'
                exp = -exp

            string += f' {symbol} {display(name)}'
            if exp != 1:
                string += '**'
                string += f'({exp})' if use_brackets else f'{exp}'
        return string.removeprefix('1 * ')

    def _json_dim(self):
        return [[name, float(exp)] for name, exp in self.items()]

    def __json__(self):
        return {
            'names': list(set(display.dimension_names.get(self, []))),
            'dimension': self._json_dim(),
        }

    def __repr__(self):
        string = self.as_fundamental()
        names = display.dimension_names.get(self, [])
        if names:
            string += '  # {}'.format(', '.join(names))
        return string

    def canonical_name(self):
        names = display.dimension_names.get(self, [])
        if names:
            return names[0]
        return self.as_fundamental()

    def __rich__(self):
        if self.is_fundamental():
            reprs = f'[bold italic]{self.keys()[0]}[/]'
        else:
            reprs = f'[italic]{self.as_fundamental()}[/]'

        names = display.dimension_names.get(self, [])
        if names:
            return f'[bold italic]{names[0]}[/] ({reprs})'

        return reprs

    # Operations

    def __bool__(self):
        return not all(i == 0 for i in self.values())

    def __pow__(self, exp):
        exp = Fraction(exp)
        return Dimension({k: v*exp for k, v in self.items()})

    # Multiplication

    def _extract_dimension(self, other):
        if isinstance(other, Number):
            return Dimension()
        if isinstance(other, Dimension):
            return other
        elif isinstance(other, Unit):
            return other.dim
        else:
            n = type(other).__name__
            raise TypeError(f"Cannot operate on Dimension with {n}")

    def __mul__(self, other, op=+1):
        other = self._extract_dimension(other)
        names = set(self.keys()) | set(other.keys())
        return Dimension({
            n: self.get(n, 0) + op * other.get(n, 0)
            for n in names
        })
    __rmul__ = __mul__

    def __truediv__(self, other):
        return self.__mul__(other, -1)

    def __rtruediv__(self, other):
        return self._extract_dimension(other) / self

    # Linear ops

    def _linear_operation(self, other):
        other = self._extract_dimension(other)
        if self == other:
            return self
        else:
            raise DimensionError(
                f'Dimensions {self} and {other} do not match')

    __sub__ = __rsub__ = __add__ = __radd__ = _linear_operation


dimensionless = Dimension()

# Avoid import loops
from .Unit import Unit  # noqa
from .DisplaySet import display  # noqa
