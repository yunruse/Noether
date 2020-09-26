import fractions
import numbers
from abc import ABC, abstractmethod
CF_FACTORS_IN_STR = 20
CF_FACTORS_IN_FLOAT = 30
CF_FLOAT_ERROR = 1e-11


class GenericFraction(ABC):
    function = None
    repeat = 0

    @property
    @abstractmethod
    def factors(self):
        pass

    def __getitem__(self, i):
        if isinstance(i, slice):
            return tuple(self[j] for j in (
                range(i.start, i.stop, i.step) if i.step else (
                    range(i.start, i.stop) if i.start else
                    range(i.stop))))

        if callable(self.function):
            return self.function(i)

        l, r = len(self.factors), self.repeat
        if l == i == 0:
            return 0
        elif i < l:
            return self.factors[i]
        elif not r:
            return 0
        else:
            # wrap around ignoring initial constant factors
            c = l - r
            j = i - c
            return self.factors[c + (j % r)]


class ContinuedFraction(GenericFraction):
    ''''''
    __slots__ = ('factors', 'repeat', 'function')

    def __new__(cls, numerator=0, denominator=None, *factors, repeat=0, _normalize=True):
        self = object.__new__(cls)
        self.function = None
        self.repeat = repeat

        if callable(numerator):
            self.factors = None
            self.function = numerator
            return self

        elif not isinstance(numerator, numbers.Rational):
            if factors or denominator is not None:
                raise TypeError(
                    'multiple factors must all be Rational instances')
            self.factors = []
            num = 0
            diff = numerator
            for n in range(CF_FACTORS_IN_FLOAT):
                num, diff = divmod(diff, 1)
                self.factors.append(int(num))
                if diff < CF_FLOAT_ERROR:
                    break
                diff = 1 / diff

            if repeat:
                # if given a float, 'repeat' means digits
                _, digits = str(numerator).split('.')
                a = int(digits[-repeat:])
                b = 10 ** -len(digits)
                repeator = ContinuedFraction(a, b).factors
                print(a, b, repeator)
                self.factors += repeator
                self.repeat = len(repeator)
            self.factors = tuple(self.factors)
            return self
        else:
            self.factors = (numerator, denominator, *
                            factors) if denominator else (numerator, )
            if not all(isinstance(i, numbers.Rational) for i in factors):
                raise TypeError(
                    'multiple factors must all be Rational instances')
            return self.normalize() if _normalize else self

    def normalize(self):
        '''
        Return a normalized version of the repeating fraction.

        This is done on creation unless
        '''
        if self.repeat:
            static, repeating = self.factors[:-
                                             self.repeat], self.factors[-self.repeat:]
        else:
            static = self.factors
            repeating = tuple()

        nstatic = list()
        nrepeating = list(repeating)
        i = 0
        while i < len(static):
            if static[i] == 0 and i + 1 < len(static) and static[i+1] == 0:
                # x + 1/(0 + 1/(0 + y)) is equivalent to x + 1/y
                i += 2
                continue
            nstatic.append(static[i])
            i += 1

        return ContinuedFraction(*(nstatic + nrepeating), repeat=len(repeating), _normalize=False)

    def __repr__(self):
        if callable(self.function):
            return '{}(<irrational function>)'.format(
                type(self).__name__)

        return '{}({}{})'.format(
            type(self).__name__,
            ', '.join(map(str, self.factors)),
            ', repeat={}'.format(self.repeat) if self.repeat else ''
        )

    def __str__(self):
        if callable(self.function):
            n = CF_FACTORS_IN_STR
            nonterminated = True
        else:
            n = len(self.factors) + self.repeat
            if n < 2:
                return str(self[0])
            nonterminated = self.repeat
            if n > CF_FACTORS_IN_STR:
                n = CF_FACTORS_IN_STR
                nonterminated = True
        return '[{}; {}{}]'.format(
            self[0], ', '.join(str(self[i]) for i in range(1, n)),
            '...' * nonterminated
        )

    def __round__(self):
        a, b, c = self[0:3]
        return a + 1 if b == 1 and c else a

    def __int__(self):
        return self[0]

    def __floor__(self):
        return self[0]

    def __float__(self):
        if self.factors and len(self.factors) < 2:
            return float(self[0])
        num = 0.0
        factors = CF_FACTORS_IN_FLOAT if self.function or self.repeat else len(
            self.factors)
        for i in range(factors-1, 0, -1):
            num += self[i]
            num = 1 / num
        return self[0] + num


class Fraction(fractions.Fraction, GenericFraction):
    '''
    This class implements rational numbers, and can form continued fractions.
    >>> Fraction(1)
    1
    >>> Fraction
    '''
    factors = property(lambda x: (x.numerator, x.denominator))

    def __new__(cls, numerator=0, denominator=None, *factors, repeat=0, _normalize=True):
        if factors or repeat or not isinstance(numerator, numbers.Rational):
            return ContinuedFraction(
                numerator, denominator, *factors, repeat=repeat, _normalize=_normalize)
        else:
            return fractions.Fraction.__new__(cls, numerator, denominator, _normalize=_normalize)


e = Fraction(lambda i: 2 if i == 0 else 2*(1+i//3) if i % 3 == 2 else 1)
