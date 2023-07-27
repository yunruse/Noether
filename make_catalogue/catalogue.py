from dataclasses import dataclass, field
from pathlib import Path

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .types import Definition, Def


@dataclass
class Catalogue:
    definitions: list[Def] = field(default_factory=list)

    @classmethod
    def from_path(cls, path: Path):
        self = cls()

        for noe_path in path.glob('**/*.yaml'):
            with open(noe_path) as f:
                for d in load(f, Loader):
                    self.definitions.append(Definition(d))

        return self
