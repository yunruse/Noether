from collections import namedtuple
from fractions import Fraction
from numbers import Number
from typing import Callable

from noether.Multiplication import Multiplication

from ..config import conf
from ..helpers import ImmutableDict, removeprefix, reorder_dict_by_values
from ..errors import NoetherError, DimensionError


BaseDimension = str
DimInfo = namedtuple('DimInfo', ('order', 'symbol'))


class Dimension(Multiplication[BaseDimension]):
    '''
    Dimension of a unit.

    Internally, a dict of names to Fractions.
    The dimension names are stored in _names,
    alongside their display order.
    '''

    # Class variable with display order
    _names: dict[BaseDimension, DimInfo] = dict()

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
        self = cls({name: Fraction(1)})
        display.add(self, name)
        return self

    def is_base_dimension(self):
        '''True iff the dimension is a base dimension'''
        return list(self.values()) == [Fraction(1)]

    def items(self):
        exponents = list(super().items())
        # positive first, then negative
        exponents.sort(key=lambda q: (q[1] < 0, self._names[q[0]].order))
        return exponents

    # |~~\ '      |
    # |   ||(~|~~\|/~~|\  /
    # |__/ |_)|__/|\__| \/
    #         |        _/

    def as_fundamental(
        self, /,
        display: Callable[[str], str] = lambda x: x
    ):
        if not self:
            return display('dimensionless')

        string = '1'
        for name, exp in self.items():
            symbol = '*'
            use_brackets = exp.denominator != 1
            if not use_brackets and exp < 0:
                symbol = '/'
                exp = -exp

            string += f' {symbol} {display(name)}'
            if exp != 1:
                string += '**'
                string += f'({exp})' if use_brackets else f'{exp}'
        return removeprefix(string, '1 * ')

    def canonical_name(self):
        names = display.dimension_names.get(self, [])
        if names:
            return names[0]
        return self.as_fundamental()

    def __repr__(self):
        if conf.get('display_repr_code'):
            return super().__repr__()
        return self.__noether__()

    def __noether__(self):
        string = self.as_fundamental()
        names = display.dimension_names.get(self, [])
        if names:
            string += '  # {}'.format(', '.join(names))
        return string

    def __rich__(self):
        if self.is_base_dimension():
            return f'[bold italic]{list(self.keys())[0]}[/]'

        reprs = self.as_fundamental()

        names = display.dimension_names.get(self, [])
        if names:
            return f'[bold italic]{names[0]}[/]  [green italic]# {reprs}'

        return reprs

    def __str__(self):
        return self.canonical_name()

    def _json_dim(self):
        return sorted([name, float(exp)] for name, exp in self.items())

    def __json__(self):
        return {
            'names': sorted(set(display.dimension_names.get(self, []))),
            'dimension': self._json_dim(),
        }


dimensionless = Dimension()

# Avoid import loops
from .Unit import Unit  # noqa
from .DisplaySet import display  # noqa
