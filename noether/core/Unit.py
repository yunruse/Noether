'''
Unit - a subclass of Measure which has its own name(s) and symbol(s).

Used in turn to display Measure.
'''

from .config import conf
from .display import canonical_number
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

    @property
    def symbol(self):
        if self.symbols:
            return self.symbols[0]
        if self.names:
            return self.names[0]
        return self.as_fundamental()

    @property
    def name(self):
        if self.names:
            return self.names[0]
        if self.symbols:
            return self.symbols[0]
        return self.as_fundamental()

    # |~~\ '      |
    # |   ||(~|~~\|/~~|\  /
    # |__/ |_)|__/|\__| \/
    #         |        _/

    def __repr__(self):
        if conf.get('display_repr_code'):
            return self.repr_code()
        return self.__noether__()

    def repr_code(self):
        chunks = [Measure.repr_code(self)]
        for i in self.names, self.symbols:
            if len(i) == 0:
                chunks.append('None')
            if len(i) == 1:
                chunks.append(repr(i[0]))
            else:
                chunks.append(repr(i))
        if self.prefixes:
            chunks.append(repr(self.prefixes))
        return 'Unit({})'.format(', '.join(chunks))

    def __noether__(self):
        return f"{self.name}  # {self.dim.canonical_name()}"

    def __rich__(self):
        string = (
            f"[bold]{self.name}[/]"
            f"[italic green]  # {self.dim.canonical_name()}[/]")
        d = self.display_unit()
        if d != self:
            if d is None:
                d = self * 1
            string += f", [italic blue]{d.repr_measure(self)}"
        return string

    def __str__(self):
        return self.name

    def _json_extras(self):
        return {}

    def __json__(self):
        json = {
            'value': self.value,
            'stddev': self.stddev,
            'dimension': self.dim._json_dim(),
            'names': self.names,
            'symbols': self.symbols,
        }
        json.update(self._json_extras())
        if self.stddev is None:
            del json['stddev']
        if self.prefixes:
            json['prefixes'] = self.prefixes.name.split(' + ')
        return json

    def repr_measure(self, measure: Measure):
        val = measure.value / self.value
        stddev = None
        if measure.stddev is not None:
            stddev = measure.stddev / self.value

        v = canonical_number(val, stddev)
        return f'{v} {self.symbol}'


from .DisplaySet import display  # noqa
