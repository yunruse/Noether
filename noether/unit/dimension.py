"""Noether: Measure Dimension"""

import bisect
from collections import namedtuple

from ..helpers import intify
from .scale import superscript
from .measure import Unit

_BaseDimension = namedtuple("_BaseDimension", "order name display_unit".split())


class Dimension(dict):
    """Dimension of a unit. Inherently immutible."""
    _dimensions_display = list()
    _dimensions_map = dict()

    def __init__(self, value=None, **kw):
        value = value or dict()

        if isinstance(value, dict):
            value = value
        elif isinstance(value, Unit):
            value = value.dim
        
        value.update(kw)
        dims = value.copy()
        
        for name, exp in value.items():
            if not exp:
                del dims[name]
            if name not in self._dimensions_map:
                raise ValueError(
                    "Unknown dimension {!r}. Did you register it with .new?"
                    .format(name))

        dict.__init__(self, dims)

    @classmethod
    def new(cls, order, name, display_unit):
        base = _BaseDimension(order, name, display_unit)
        bisect.insort_left(cls._dimensions_display, base)
        cls._dimensions_map[name] = base
        return cls({name: 1})
    
    # Immutability   
    
    def __setitem__(self, name, value):
        raise TypeError('{!r} object does not support item assignment'.format(type(self).__name__))
    def __delitem__(self, name):
        raise TypeError('{!r} object does not support item deletion'.format(type(self).__name__))
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
    
    # Name registry (such that generated Dimensions map)

    _names = dict()

    @property
    def names(self):
        return self._names.get(self, list())
    
    def addName(self, name):
        name = name.replace('_', ' ')
        if self not in self._names:
            self._names[self] = list()
        self._names[self].append(name)
    
    # Reproduction

    def asFundamentalUnits(self):
        dims = []
        for _, name, sym in self._dimensions_display:
            exp = self.get(name, 0)
            if exp == 0:
                continue
            elif exp != 1:
                if Unit.unicodeExponent:
                    sym += str(exp).translate(superscript)
                else:
                    sym += "^" + str(exp)
            dims.append(sym)

        return "·".join(dims)

    def __str__(self):
        # TODO: return actual E-T-M etc units
        return self.asFundamentalUnits()

    def __repr__(self):
        exponents = sorted(list(self.items()), key=lambda q: (q[1] < 0, abs(q[1])))
        string = '1' if exponents[0][1] < 0 else ''
        for dim, exp in exponents:
            if string:
                string += ' / ' if exp < 0 else ' * '
            aexp = abs(exp)
            if aexp == 1/2:
                string += 'sqrt('+dim+')'
                continue
            string += dim
            if aexp != 1:
                string += '**' + str(aexp)
        return string
    
    # Operations

    def __bool__(self):
        return not all(i == 0 for i in self.values())

    def __pow__(self, exp):
        if isinstance(exp, (int, float)):
            return Dimension({k: intify(v * exp) for k, v in self.items()})
        else:
            raise TypeError("Cannot raise dimension to non-real exponent")

    def _cmp(self, other):
        """Check and attempt to match other unit to Dimension"""
        if isinstance(other, (float, int)):
            return Dimension()
        if isinstance(other, Dimension):
            return other
        elif isinstance(other, Unit):
            return other.dim
        else:
            raise TypeError("Cannot operate on Dimension with {}".format(
                type(other).__name__))

    def __mul__(self, other, op=+1):
        other = self._cmp(other)
        names = set(self.keys()).union(set(other.keys()))
        return Dimension(
            {n: self.get(n, 0) + op * other.get(n, 0)
             for n in names})

    def __truediv__(self, other):
        return self.__mul__(other, -1)

    def __rtruediv__(self, exp):
        return self._cmp(exp) / self

    __rmul__ = __mul__
    __pos__ = __neg__ = lambda s: s

    def _checkLinear(self, other):
        other = self._cmp(other)
        if self == other:
            return self
        else:
            raise ValueError(
                "Cannot add or subtract inequal dimensions {} and {}".
                format(self, other))

    __sub__ = __rsub__ = __add__ = __radd__ = _checkLinear
