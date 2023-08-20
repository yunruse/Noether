from typing import Iterable

from .Prefix import Prefix


class PrefixSet(set[Prefix]):
    __slots__ = ('name', )

    def __init__(self, name: str, prefixes: Iterable[Prefix] | None = None):
        self.name = name
        super().__init__(prefixes or [])

    def __or__(self, other: 'PrefixSet'):
        return PrefixSet(
            f'{self.name} | {other.name}',
            set(self) | set(other))

    def __repr__(self):
        return f'PrefixSet({self.name!r}, {set(self)!r})'

    def __json__(self):
        return {'name': self.name, 'prefixes': [p.__json__() for p in self]}
