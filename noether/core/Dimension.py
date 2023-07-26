from collections import namedtuple
from fractions import Fraction
from functools import wraps
from typing import ClassVar

from noether.helpers import Rational
from noether.helpers import reorder_dict_by_values
from noether.Multiplication import Multiplication

from noether.display import DISPLAY_REPR_CODE

from ..config import conf


BaseDimension = str
DimInfo = namedtuple('DimInfo', ('order', 'symbol'))
BaseDimDict = dict[BaseDimension, Rational]


class Dimension(Multiplication[BaseDimension]):
    '''
    Dimension of a unit, such as time, speed or temperature.
    '''

    # Known base dimensions
    _known_dimensions: ClassVar[dict[BaseDimension, DimInfo]] = dict()

    # Known composed dimension names
    _names: ClassVar[dict['Dimension', list[str]]] = dict()

    # Instantiation

    def __init__(
        self,
        dimensions: BaseDimension | BaseDimDict | None = None,
        *names: str
    ):
        dims: BaseDimDict = {}
        if isinstance(dimensions, BaseDimension):
            dims = {dimensions: 1}
        elif isinstance(dimensions, dict):
            dims = dimensions
            well_formed = all(
                isinstance(d, BaseDimension)
                and d in type(self)._known_dimensions
                for d, exp in dimensions.items()
            )
            if not well_formed:
                raise TypeError(
                    "Malformed Dimension."
                    " Use e.g. `length = Dimension.new(...)`"
                    " and compose derived dimensions.")

        super().__init__(dims)
        self._names.setdefault(self, [])
        self._names[self].extend(names)

    @classmethod
    def new(
        cls,
        name: BaseDimension,
        symbol: str,
        order: float = 0,
    ):
        '''
        Register a new base dimension and return its unit.
        '''
        cls._known_dimensions[name] = DimInfo(order, symbol)
        reorder_dict_by_values(cls._known_dimensions)
        self = cls({name: Fraction(1)}, name)
        display.display(self)
        return self

    def is_base_dimension(self):
        '''True iff the dimension is a base dimension'''
        return list(self.values()) == [Fraction(1)]

    def items(self):
        exponents = list(super().items())
        # positive first, then negative
        exponents.sort(key=lambda q: (
            q[1] < 0, self._known_dimensions[q[0]].order))
        return exponents

    # |~~\ '      |
    # |   ||(~|~~\|/~~|\  /
    # |__/ |_)|__/|\__| \/
    #         |        _/

    @wraps(Multiplication.display)
    def display(self, **kwargs):
        kwargs.setdefault('identity_string', 'dimensionless')
        return super().display(**kwargs)

    @property
    def symbol(self):
        return super().display(
            display_function=lambda b: self._known_dimensions[b].symbol,
            drop_multiplication_signs=True,
            identity_string='1'
        )

    @property
    def order(self):
        if self.is_base_dimension():
            k = list(self)[0]
            return self._known_dimensions[k].order
        # TODO: could this be more specific?
        return 999

    @property
    def names(self):
        # TODO: Fetch for equality..?
        return self._names[self]

    def name(self):
        if self.names:
            return self.names[0]
        return self.display()

    def _repr_code(self):
        return super().__repr__()

    def __repr__(self):
        if conf.get(DISPLAY_REPR_CODE):
            return super().__repr__()
        return self.__noether__()

    def __noether__(self):
        string = self.display()
        if self.names:
            string += '  # {}'.format(', '.join(self.names))
        return string

    def __rich__(self):
        if self.is_base_dimension():
            return f'[bold italic]{list(self.keys())[0]}[/]'

        reprs = self.display()

        if self.names:
            return f'[bold italic]{self.names[0]}[/]  [green italic]# {reprs}'

        return reprs

    def __str__(self):
        return self.name()

    def _json_dim(self):
        return sorted([name, float(exp)] for name, exp in self.items())

    def __json__(self):
        return {
            'names': sorted(self.names),
            'dimension': self._json_dim(),
        }


dimensionless = Dimension()

# Avoid import loops
from ._DisplayHandler import display  # noqa
