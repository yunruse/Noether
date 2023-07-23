'''
Generic (Noether-nonspecific) expression for multiplication, division and exponentiation.

Internally used for such compostions as Dimension and ChainedUnit.
'''

from math import prod
from typing import Callable, Generic, TypeVar

from noether.helpers import Rational, Real
from noether.helpers import ImmutableDict, removeprefix


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

    def items_positive_first(self):
        return sorted(super().items(), key=lambda q: (-q[1], q[0]))

    def __bool__(self):
        return any(x != 0 for x in self.values())

    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    # % Geometric ops

    def _geo(self, value: T | 'Multiplication[T]', direction: int):
        if isinstance(value, Multiplication):
            return type(self)({
                x: exp for x in set(self) | set(value)
                if (exp := self.get(x, 0) + value.get(x, 0)*direction)
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

    def __pow__(self, exponent: Real):
        return type(self)({
            value: i * exponent
            for value, i in self.items()
        })

    # % Display

    def display(
        self, /,
        display_function: Callable[[T], str] = lambda x: str(x or 1),
        use_slashes=True,
        drop_multiplication_signs=False,
        identity_string='1',
    ):
        '''
        Display e.g. x**2 * y**3 or meter / second.
        Returns identity_string if empty (multiplative identity, aka 1).
        '''
        if not self:
            return identity_string

        string = '1'
        for name, exp in self.items():
            if not exp:
                continue
            symbol = '*'
            use_brackets = hasattr(exp, 'denominator') and exp.denominator != 1
            if use_slashes and not use_brackets and exp < 0:
                symbol = '/'
                exp = -exp

            string += f' {symbol} {display_function(name)}'
            if exp != 1:
                # TODO: unicode exponents
                string += '**'
                string += f'({exp})' if use_brackets else f'{exp}'

        string = removeprefix(string, '1 * ')
        if drop_multiplication_signs:
            string = string.replace(' * ', ' ')

        return string

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, dict.__repr__(self))


T_mult = TypeVar('T_mult', Real, Rational)


class MultiplicationWithValue(Generic[T_mult], Multiplication[T_mult]):
    '''
    Multiplication with a value.
    T must support multiplication and exponentiation.
    '''

    def value(self):
        return prod(item ** exponent for item, exponent in self.items())
