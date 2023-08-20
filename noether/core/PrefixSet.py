from typing import Iterable

from ..helpers import Real, removesuffix

from .Prefix import Prefix


class PrefixSet(set[Prefix]):
    __slots__ = ('name', )

    def __init__(self, name: str, prefixes: Iterable[Prefix] | None = None):
        self.name = name
        super().__init__(prefixes or [])

    def __repr__(self):
        return f'PrefixSet({self.name!r}, {set(self)!r})'

    def __json__(self):
        return {'name': self.name, 'prefixes': [p.__json__() for p in self]}

    # Compositions

    def hidden(self):
        "Return a copy where all display=False."
        return PrefixSet(
            f'{self.name}.hidden()', {
                Prefix(p.prefix, p.symbol, p.value, display=False)
                for p in self
            })

    def __or__(self, other: 'PrefixSet'):
        return PrefixSet(
            f'{self.name} | {other.name}',
            set(self) | set(other))

    # Representation of other values

    def _displayable_prefixes(self):
        return sorted(
            (p for p in self if p.display),
            key=lambda p: p.value)

    def with_prefix(self, num: Real) -> tuple[Real, Prefix | None]:
        """
        Obtain the prefix (or None) and corresponding number that best represent the value provided.

        >>> IEC.with_prefix(2048)
        (2.0, Prefix(prefix='kibi', symbol='Ki', value=1024))
        """
        prefix: Prefix | None = None
        for p in self._displayable_prefixes():
            if p.value > num:
                break
            prefix = p

        if prefix is None or (prefix.value < 1 and num >= 1):
            return num, None

        return num / prefix.value, prefix

    def repr_num(self, num: Real, fmt: str | None = None):
        """
        Represent a number according to the best matching prefix (or no prefix).
        Takes an optional formatter code (e.g. '.3f')

        >>> IEC.repr_num(2048)
        '2 Ki'
        """
        num, prefix = self.with_prefix(num)
        if fmt is not None:
            n = format(num, fmt)
        else:
            n = removesuffix(str(num), '.0')

        if prefix is not None:
            return f'{n} {prefix.symbol}'
        return n
