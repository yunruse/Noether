'''
Unit - a subclass of Measure which has its own name(s) and symbol(s).

Used in turn to display Measure.
'''

from ..config import conf
from ..display import canonical_number
from .prefixes import Prefix
from .Dimension import Dimension
from .Measure import Measure, MeasureInfo


class Unit(Measure):
    __slots__ = 'value stddiv dim symbols names prefixes info'.split()

    names: tuple[str]
    prefixes: list[Prefix]
    info: str

    def __init__(
        self,
        measure: Measure | Dimension,
        names: list[str] | str | None = None,
        symbols: list[str] | str | None = None,
        prefixes: list[Prefix] | None = None,
        info: str | None = None,
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
        setattr('info', info or None)

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

        v = canonical_number(val, stddev)
        return f'{v} {self.symbol}'


@Measure.Info
class info_unit_value(MeasureInfo):
    '''Give unit values, rather than just the bare name.'''
    style = 'italic blue'

    @classmethod
    def info(self, measure: 'Unit') -> str:
        if isinstance(measure, Unit):
            d = measure.display_unit()
            if d != measure:
                if d is None:
                    d = measure * 1
                yield d.repr_measure(measure)


@Measure.Info
class info_unit_context(MeasureInfo):
    '''Give additional context for units from their .info attribute.'''
    style = 'red underline'

    @classmethod
    def info(self, measure: 'Unit') -> str:
        if isinstance(measure, Unit) and measure.info is not None:
            yield measure.info
