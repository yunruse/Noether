'''
Unit - a subclass of Measure which has its own name(s) and symbol(s).

Used in turn to display Measure.
'''

from .prefixes import Prefix
from .Dimension import Dimension
from .Measure import Measure


class Unit(Measure):
    __slots__ = 'value stddiv dim symbols names prefixes'.split()

    names: tuple[str]
    symbols: tuple[str]
    prefixes: set[str]

    def __init__(
        self,
        measure: Measure | Dimension,
        names: list[str] | str | None = None,
        symbols: list[str] | str | None = None,
        prefixes: list[Prefix] | None = None
    ):
        if isinstance(measure, Dimension):
            measure = Measure(dim=measure)
        super().__init__(measure)

        def setattr(x, v):
            # bypass Frozen
            object.__setattr__(self, x, v)

        for k, v in ('names', names), ('symbols', symbols):
            setattr(k, (v, ) if isinstance(v, str) else v or [])
        setattr('prefixes', prefixes or [])

    def __repr_code__(self):
        chunks = [Measure.__repr__(self)]
        for i in self.names, self.symbols:
            if len(i) == 1:
                chunks.append(repr(i[0]))
            else:
                chunks.append(repr(i))
        if self.prefixes:
            chunks.append(repr(self.prefixes))
        return 'Unit({})'.format(', '.join(chunks))

    def __str__(self):
        return f'{self.names[0]} ({self.dim!r})'

    def __rich__(self):
        return f'[bold]{self.names[0]}[/] ([italic]{self.dim.canonical_name()}[/])'
