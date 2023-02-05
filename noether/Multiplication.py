'''
Generic (Noether-nonspecific) expression for multiplication, division and exponentiation.

Internally used for such compostions as Dimension and ChainedUnit.
'''

from math import prod
from numbers import Rational
from typing import Generic, TypeVar

from noether.helpers import ImmutableDict


T = TypeVar('T')


class Multiplication(Generic[T], ImmutableDict[T, Rational]):
    '''
    Expression which encapsulates multiplication, division and exponentiation.
    T need not support these operations intrinsically - a Multiplication is designed to hold its terms, not evaluate them.
    If T does support these values, however, MultiplicationWithValue provides this extra functionality. 
    '''
    __slots__ = tuple()

    def __init__(self, value: T | dict[T, Rational] | None = None):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            value = {value: 1}
        super().__init__(value)

    def __bool__(self):
        return not any(x == 0 for x in self.values())

    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    # % Geometric ops

    def _geo(self, value: T | 'Multiplication[T]', direction: int):
        if isinstance(value, Multiplication):
            return type(self)({
                x: self.get(x, 0) + value.get(x, 0)*direction
                for x in set(self) | set(value)
            })

        else:
            new = dict(self)
            new.setdefault(value, 0)
            new[value] += direction
            return type(self)(new)

    def __mul__(self, value: T | 'Multiplication[T]'):
        return self._geo(value, +1)

    def __truediv__(self, value: T | 'Multiplication[T]'):
        return self._geo(value, -1)

    def __rtruediv__(self, value: int):
        if value == 1:
            # 1 / x  ==  x ** -1
            return self ** -1

        return NotImplemented

    def __pow__(self, exponent: Rational):
        return type(self)({
            value: i * exponent
            for value, i in self.items()
        })

    # % Display

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, dict.__repr__(self))


class MultiplicationWithValue(Generic[T], Multiplication[T]):
    '''
    Multiplication with a value.
    T must support multiplication and exponentiation.
    '''

    def value(self):
        return prod(item ** exponent for item, exponent in self.items())
