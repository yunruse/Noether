'''
Unit - a subclass of Measure which has its own name(s) and symbol(s).

Used in turn to display Measure.
'''

from datetime import timedelta
from itertools import chain
from noether.helpers import Rational, Real, removeprefix

from ..errors import NoetherError
from ..config import conf
from ..display import DISPLAY_REPR_CODE, canonical_number
from .Prefix import PrefixSet
from .Dimension import Dimension
from .Measure import Measure, UNCERTAINTY_SHORTHAND


class Unit(Measure):
    __slots__ = '_value stddiv dim symbols names prefixes info'.split()

    names: list[str]
    symbols: list[str]
    prefixes: PrefixSet
    info: str

    def __init__(
        self,
        measure: Real | Measure | Dimension | timedelta,
        names: str | list[str] | None = None,
        symbols: str | list[str] | None = None,
        prefixes: PrefixSet | None = None,
        info: str | None = None,
    ):
        if isinstance(measure, Dimension):
            measure = Measure(dim=measure)
        super().__init__(measure)

        def setattr(x, v):
            # bypass Frozen
            object.__setattr__(self, x, v)

        for k, v in ('names', names), ('symbols', symbols):
            setattr(k, [v] if isinstance(v, str) else v or [])

        setattr('prefixes', prefixes or [])
        setattr('info', info or None)

        from ..core import display
        if self.dim.is_base_dimension() and not self.dim in display.dimension_units:
            # ensure the first defined unit for a dimension is used for display
            # to avoid catastrophic glitches
            if not len(self.symbols):
                raise NoetherError(
                    f'Symbol required for first unit defined for {self.dim.name()}')

            display(self)

    # Useful cataloguing tools

    def prefixed_units(self):
        for prefix in self.prefixes:
            yield prefix * self

    def _namespace(self):
        return {x: self for x in chain(self.names, self.symbols)}

    # Nicer display units

    def __mul__(self, value: Measure | Real) -> Measure:
        return GeometricUnit(self) * value  # type: ignore

    def __truediv__(self, value: Measure | Real) -> Measure:
        return GeometricUnit(self) / value  # type: ignore

    def __pow__(self, value: Rational) -> Measure:
        return GeometricUnit(self) ** value

    def _fallback_display(self) -> str:
        from ._DisplayHandler import display

        unit = self.dim.display(
            display_function=lambda x: display._dimension_symbol[x],
            drop_multiplication_signs=True,
            identity_string='',
        )

        return removeprefix(unit, '1 ')  # avoid "2  1 / m"

    @property
    def symbol(self):
        if self.symbols:
            return self.symbols[0]
        if self.names:
            return self.names[0]
        return self._fallback_display()

    @property
    def name(self):
        if self.names:
            return self.names[0]
        if self.symbols:
            return self.symbols[0]
        return self._fallback_display()

    # |~~\ '      |
    # |   ||(~|~~\|/~~|\  /
    # |__/ |_)|__/|\__| \/
    #         |        _/

    def __repr__(self):
        if conf.get(DISPLAY_REPR_CODE):
            return self._repr_code()
        return self.__noether__()

    def _repr_code(self):
        chunks = [Measure._repr_code(self)]
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

    def _json_extras(self):
        return {}

    def __json__(self):
        json = {
            'value': self._value,
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

    def _repr_measure(self, measure: Real | Measure):
        if isinstance(measure, Measure):
            val = measure._value / self._value
            stddev = None
            if measure.stddev is not None:
                stddev = measure.stddev / self._value
        else:
            val: Real = measure  # type: ignore
            stddev = None

        v = canonical_number(val, stddev, conf.get(UNCERTAINTY_SHORTHAND))
        if self.dim or self.symbols:
            v += ' ' + self.symbol
        return v

    def __and__(self, unit: 'Unit'):
        from .units.LinearUnit import LinearUnit
        return LinearUnit([self, unit])


# Avoid import loops
from .units.GeometricUnit import GeometricUnit  # noqa
