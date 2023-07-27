from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .types import *

T = TypeVar('T')


class Catalogue(dict[type, list[CatalogueDef]]):
    @classmethod
    def from_path(cls, path: Path):
        self = cls()
        for noe_path in path.glob('**/*.yaml'):
            with open(noe_path) as f:
                for d in load(f, Loader):
                    d = Definition(d)
                    self.append(d)
        return self

    def append(self, value):
        t = type(value)
        self.setdefault(t, [])
        self[t].append(value)

    def get(self, t: type[T]) -> list[T]:
        return dict.get(self, t, [])

    _bd: dict[str, BaseDimensionDef]
    _d: dict[str, DimensionDef]

    def _evaluate_dimensions(self):
        _BD = self.get(BaseDimensionDef)
        self._bd = {d.basedimension: d for d in _BD}

        # get names

        self._d = {}
        for d in self.get(DimensionDef):
            for n in d.names:
                self._d[n] = d

            # evaluate Multiplication
            d.value = Multiplication.from_string(d.dimension)
            for name in d.value.keys():
                if not (name in self._d or name in self._bd):
                    raise NameError('Unknown dimension name', name)

    _p: dict[str, PrefixDef]
    _ps: dict[str, PrefixSetDef]

    def _evaluate_prefixes(self):
        for ps in self.get(PrefixSetDef):
            for p in ps.prefixes:
                self.append(p)

        self._p = {p.prefix: p for p in self.get(PrefixDef)}
        self._ps = {p.prefixset: p for p in self.get(PrefixSetDef)}

        for ps in self.get(PrefixSetDef):
            ps.names = [p.prefix for p in ps.prefixes]

        for ps in self.get(PrefixSetDef):
            for inc in ps.includes:
                ps.names += self._ps[inc].names

    def evaluate(self):
        self._evaluate_prefixes()
        self._evaluate_dimensions()

    def _render_lines(self):
        yield '# Automatically generated from .yaml files'

        yield 'from noether import Dimension, Prefix, PrefixSet'

        for p in self.get(PrefixDef):
            yield '{} = Prefix({!r}, {!r}, {})'.format(
                p.prefix, p.prefix, p.symbol, p.value
            )

        for ps in self.get(PrefixSetDef):
            yield '{} = PrefixSet({!r}, {{{}}})'.format(
                ps.prefixset, ps.prefixset,
                ', '.join(ps.names)
            )

        for b in self.get(BaseDimensionDef):
            n = b.basedimension
            yield f'{n} = Dimension.new({n!r}, {b.symbol!r})'

        for d in self.get(DimensionDef):
            yield '{} = Dimension({}, {})'.format(
                ' = '.join(d.names),
                d.dimension,
                ', '.join(map(repr, d.names))
            )

    def render(self):
        self.evaluate()
        return '\n'.join(self._render_lines())


# render procedure:

# - [x] store basedimensions
# - [x] store dimensions
# - [x] evaluate dimensions (Multiplication)

# - [ ] store prefixes
# - [ ] collect prefixsets

# - [ ] store units
# - [ ] collect units
# - [ ] evaluate units (value + dimension)
