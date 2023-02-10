'''
Catalogue of units, which may handle interpreting
units with prefixes.
'''

from ..helpers import removeprefix
from ..config import Config, conf
from . import Dimension, Unit
from .Prefix import PrefixSet, Prefix

Config.register('UNITS_all_prefixes', False, help='''\
Allow fetching any unit with any prefix (e.g. gibimeter).''')


class Catalogue:
    dimensions: dict[str, Dimension]
    units_by_name: dict[str, Unit]
    prefix_sets: dict[str, PrefixSet]

    _prefixes = dict[str, Prefix]

    def __init__(self, catalogue: dict):
        self.units_by_name = dict()
        self.dimensions = dict()
        self.prefix_sets = dict()
        self._prefixes = dict()

        for k, v in catalogue.items():
            self.register(k, v)

    def register(self, k: str, v):
        if isinstance(v, Unit):
            self.units_by_name[k] = v
            for n in v.names:
                self.units_by_name[n] = v
            for n in v.symbols:
                self.units_by_name[n] = v
        elif isinstance(v, Dimension):
            self.dimensions[k] = v
        elif isinstance(v, PrefixSet):
            self.prefix_sets[k] = v
            for prefix in v:
                self._prefixes[prefix.prefix] = prefix
                self._prefixes[prefix.symbol] = prefix

    def get(self, name: str):
        for col in (self.prefix_sets, self.dimensions, self.units_by_name):
            if name in col:
                return col[name]

        for p, prefix in self._prefixes.items():
            if not name.startswith(p):
                continue
            unit_name = removeprefix(name, p)
            if unit_name not in self.units_by_name:
                continue
            unit = self.units_by_name[unit_name]
            if not prefix in unit.prefixes:
                if not conf.get('UNITS_all_prefixes'):
                    continue
            return prefix.value * unit

        raise NameError(
            f'No unit (or prefixed unit)'
            f' with name {name!r} could be found.')

    def __getitem__(self, name: str):
        return self.get(name)

    @property
    def all_prefixed_units(self):
        units: dict[str, Unit] = {}

        for unit in self.units_by_name.values():
            units.update(unit._namespace())
            for u in unit.prefixed_units():
                units.update(u._namespace())

        return units

    @property
    def prefixes(self):
        for prefix_set in self.prefix_sets.values():
            yield from prefix_set

    def __repr__(self):
        D = len(set(self.dimensions.values()))
        U = len(set(self.units_by_name.values()))
        P = len(list(self.prefixes))

        return (
            f'<Catalogue: {D} dimensions,'
            f' {U} units, {P} prefixes>')

    def __json__(self):
        return {
            'dimensions': [
                dim.__json__() for dim in
                sorted(
                    set(self.dimensions.values()),
                    key=lambda d: d.canonical_name()
                )
            ],
            'prefix_sets': [
                ps.__json__() for ps in
                sorted(
                    self.prefix_sets.values(),
                    key=lambda p: p.name,
                )
            ],
            'units': [
                unit.__json__() for unit in
                sorted(
                    set(self.units_by_name.values()),
                    key=lambda u: u.name
                )
            ]
        }
