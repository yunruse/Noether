from collections import namedtuple
from fractions import Fraction
from numbers import Rational
from functools import wraps

from noether.Multiplication import Multiplication

from ..config import conf
from ..helpers import reorder_dict_by_values


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

    def __init__(
        self,
        dimensions: dict[BaseDimension, Rational] | None = None,
    ):
        dimensions = dimensions or {}
        well_formed = all(
            isinstance(d, BaseDimension)
            and d in type(self)._names
            for d, exp in dimensions.items()
        )
        if not well_formed:
            raise TypeError(
                "Malformed Dimension."
                " Use e.g. `length = Dimension.new(...)`"
                " and compose derived dimensions.")

        super().__init__(dimensions)

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

    @wraps(Multiplication.display)
    def display(self, **kwargs):
        kwargs.setdefault('identity_string', 'dimensionless')
        return super().display(**kwargs)

    def as_symbols(self):
        return super().display(
            display_function=lambda b: self._names[b].symbol,
            drop_multiplication_signs=True,
            identity_string='1'
        )

    def canonical_name(self):
        names = display.dimension_names.get(self, [])
        if names:
            return names[0]
        return self.display()

    def __repr__(self):
        if conf.get('display_repr_code'):
            return super().__repr__()
        return self.__noether__()

    def __noether__(self):
        string = self.display()
        names = display.dimension_names.get(self, [])
        if names:
            string += '  # {}'.format(', '.join(names))
        return string

    def __rich__(self):
        if self.is_base_dimension():
            return f'[bold italic]{list(self.keys())[0]}[/]'

        reprs = self.display()

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
from .DisplaySet import display  # noqa
