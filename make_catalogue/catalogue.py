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
                    t = type(d)
                    self.setdefault(t, [])
                    self[t].append(d)
        return self

    def get(self, t: type[T]) -> list[T]:
        return dict.get(self, t, [])

    basedims: dict[str, BaseDimensionDef]
    dims_by_name: dict[str, DimensionDef]
    dimensions: list[DimensionDef]

    def _evaluate_dimensions(self):
        _BD = self.get(BaseDimensionDef)
        self.basedims = {d.basedimension: d for d in _BD}

        _D = self.get(DimensionDef)
        self.dimensions = []
        for d in _BD:
            n = d.basedimension
            self.dimensions.append(DimensionDef(n, [n]))
        self.dimensions.extend(_D)

        # get names

        self.dims_by_name = {}
        dimnames = set()
        for d in self.dimensions:
            for n in d.names:
                self.dims_by_name[n] = d
                dimnames.add(n)

        # evaluate Multiplication

        for d in self.dims_by_name.values():
            d.value = Multiplication.from_string(d.dimension)
            for name in d.value.keys():
                if name not in dimnames:
                    raise NameError('Unknown dimension name', name)

    def evaluate(self):
        self._evaluate_dimensions()

    def _render_lines(self):
        yield '# Automatically generated from .yaml files'
        yield 'from noether import Dimension'
        for b in self.basedims.values():
            n = b.basedimension
            yield f'{n} = Dimension.new({n!r}, {b.symbol!r})'

        for d in self.dimensions:
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
