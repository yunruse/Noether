from .distribution import Distribution

from .functions import choose, mascheroni
from scipy.integrate import quad
from math import factorial

from typing import Union
from dataclasses import dataclass


@dataclass
class Binomial(Distribution):
    n: Union[int, float]
    p: float
    def __post__init__(self):
        self.discrete = isinstance(n, int)
        
    def pmf(self, k):
        if 0 <= k <= self.n:
            return (
                choose(self.n, self.k, exact=self.discrete)
                * self.p**k * (1-self.p)**(self.n-k)
            )
        return 0
    
    def cdf_continuous(self, k):        
        return quad(
            lambda t: t**(n-k-1) * (1-t)**k,
            0, 1-p
        ) * (n - k) * choose(self.n, self.k, exact=False)

@dataclass
class ChiSquared(Distribution):
    k: int
    def __post__init__(self):
        self.discrete = isinstance(k, int)
        
    def pmf(self, x):
        if x <= 0:
            return 0
        if self.discrete:
            g = factorial(x/2)
        if 0 <= k <= self.n:
            return (
                choose(self.n, self.k, exact=self.discrete)
                * self.p**k * (1-self.p)**(self.n-k)
            )
        return 0
    
    def cdf_continuous(self, k):        
        return quad(
            lambda t: t**(n-k-1) * (1-t)**k,
            0, 1-p
        ) * (n - k) * choose(self.n, self.k, exact=False)
