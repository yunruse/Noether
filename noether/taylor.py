"""Noether: Taylor polynomial generator."""

from abc import ABCMeta, abstractmethod
from math import factorial
from astley import Name, Lambda, finalise

__all__ = "Sine Cosine".strip()


class TaylorMeta(ABCMeta):
    def evaluate(cls, x, terms=7):
        return sum(cls.term(x, i) for i in cls._range(terms))

    def compileTerms(cls, terms):
        """Return a compiled function of polynomial to x terms."""
        ivals = list(cls._range(terms))
        if not ivals:
            return lambda x: 0

        xvals = [cls._term(Name("x"), i) for i in ivals]
        result = xvals.pop(0)
        if not cls._isTermPositive(ivals.pop(0)):
            result = -result

        for i, x in zip(ivals, xvals):
            if cls._isTermPositive(i):
                result += x
            else:
                result -= xvals

        func = Lambda.fromFunction(lambda x:..., result)
        print(func)
        return func.eval()

    __call__ = evaluate
    __getitem__ = compileTerms


class Taylor(metaclass=TaylorMeta):
    """Taylor polynomial (or otherwise converging sum).

    In addition to bare evalulation as `taylor(x, terms)`,
    one can use `taylor.compileTerms(n)` to compile a
    native function to carry the operation out quicker.
    """

    @classmethod
    def term(cls, x, i):
        return (1 if cls._isTermPositive(i) else -1) * cls._term(x, i)

    @classmethod
    def converge(cls, x, terms=7):
        """Converge on the true value term-by-term via a generator."""
        total = 0
        for i in cls._range(terms):
            total += cls._term(x, i)
            yield total

    @classmethod
    def _isTermPositive(cls, i):
        """Returns True iff the term is positive, useful for simplication."""
        return True

    @classmethod
    @abstractmethod
    def _term(self, x, i):
        """Individual term in summation"""

    @classmethod
    @abstractmethod
    def _range(cls, count):
        """Range of terms, useful for skipping terms."""


class Sine(Taylor):
    @classmethod
    def _isTermPositive(cls, i):
        return (i // 2) % 2

    @classmethod
    def _term(cls, x, i):
        if i == 0:
            return 1
        elif i == 1:
            return x
        else:
            return x ** i / factorial(i)

    @classmethod
    def _range(cls, n):
        return range(1, (2 * n) + 1, 2)


class Cosine(Sine):
    @classmethod
    def _range(cls, n):
        return range(2 * n, 2)
