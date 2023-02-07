'''
Unit - a subclass of Measure which has its own name(s) and symbol(s).

Used in turn to display Measure.
'''

from datetime import timedelta
from typing import Optional

from ..config import conf
from ..display import canonical_number
from .Prefix import Prefix
from .Dimension import Dimension
from .Measure import Measure, UNCERTAINTY_SHORTHAND


class Unit(Measure):
    __slots__ = 'value stddiv dim symbols names prefixes info'.split()

    names: tuple[str]
    prefixes: list[Prefix]
    info: str

    def __init__(
        self,
        measure: Measure | Dimension | timedelta,
        names: str | list[str] | None = None,
        symbols: str | list[str] | None = None,
        prefixes: list[Prefix] | None = None,
        info: str | None = None,
    ):
        # Useful!
        if isinstance(measure, timedelta):
            from .fundamental import second  # noqa
            measure = second * measure.total_seconds()

        if isinstance(measure, Dimension):
            measure = Measure(dim=measure)
        super().__init__(measure)

        def setattr(x, v):
            # bypass Frozen
            object.__setattr__(self, x, v)

        for k, v in ('names', names), ('symbols', symbols):
            setattr(k, (v, ) if isinstance(v, str) else v or [])

        setattr('prefixes', prefixes or [])
        setattr('info', info or None)

    @property
    def symbol(self):
        if self.symbols:
            return self.symbols[0]
        if self.names:
            return self.names[0]
        return self.display()

    @property
    def name(self):
        if self.names:
            return self.names[0]
        if self.symbols:
            return self.symbols[0]
        return self.display()

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

    def __str__(self):
        return self.name

    def _display_element(self):
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
        if self.info:
            json['info'] = self.info
        return json

    def repr_measure(self, measure: Measure):
        val = measure.value / self.value
        stddev = None
        if measure.stddev is not None:
            stddev = measure.stddev / self.value

        v = canonical_number(val, stddev, conf.get(UNCERTAINTY_SHORTHAND))
        return f'{v} {self.symbol}'
