from dataclasses import dataclass, field
from pathlib import Path

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .types import *


@dataclass
class Catalogue:
    definitions: dict[type, list[Def]] = field(default_factory=dict)

    @classmethod
    def from_path(cls, path: Path):
        self = cls()

        for noe_path in path.glob('**/*.yaml'):
            with open(noe_path) as f:
                for d in load(f, Loader):
                    d = Definition(d)
                    t = type(d)
                    self.definitions.setdefault(t, [])
                    self.definitions[t].append(d)

        return self
