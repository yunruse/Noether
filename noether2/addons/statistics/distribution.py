from abc import abstractmethod
from dataclasses import dataclass
from math import floor

class Distribution:
    @abstractmethod
    def pmf(self, x) -> float:
        '''Probability mass function for a continuous distribution.'''
    
    # May be modified for class (or instance!).
    discrete: bool = False
    
    def cdf(self, x) -> float:
        '''Cumulative density function, or P(X <= x).'''
        if self.discrete:
            return sum(map(self.pmf, range(floor(x))))
        else:
            return self.cdf_continuous(x)
        return NotImplemented
    
    def cdf_continuous(self, x) -> float:
        return NotImplemented
    
    __le__ = cdf

    def __contains__(self, x) -> bool:
        return bool(self.pmf(x))
        

    # When constructing a < X < b,
    # Python substitutes `(a < X) and (X < b)`.
    # This executes GT/GE then LT/LE then a (non-hookable) boolean AND.

    # As such, if GT is followed by LT, can we anticipate this
    # to hook into this flagrant disrespect for probabilities,
    # without stopping a user doing GT then LT in a legitimate use?

    # Maybe some X.t accessor which is a subsinstance to ensure uniqueness?

    def __gt__(self, a):
        print('gt', self, a)
        return a

    def __ge__(self, a):
        pass

    def __lt__(self, a):
        print('lt', self, a)
        return a

    def __le__(self, a):
        pass

    def __eq__(self, a):
        pass

    # Let user know in docs that & | must be used over AND/OR.

    def __and__(self, a):
        pass

    def __or__(self, a):
        pass