'''
Catalogue of units, which may handle interpreting
units with prefixes.
'''

from . import Dimension, Unit
from .prefixes import PrefixSet, Prefix
from ..config import Config, conf

Config.register('units_all_prefixes', False, help='''
Allow fetching any unit with any prefix (e.g. gibimeter).''')


class Catalogue:
    dimensions: dict[str, Dimension]
    units: dict[str, Unit]
    prefix_sets: dict[str, PrefixSet]

    _prefixes = dict[str, Prefix]

    def __init__(self, catalogue: dict):
        self.units = dict()
        self.dimensions = dict()
        self.prefix_sets = dict()
        self._prefixes = dict()

        for k, v in catalogue.items():
            self.register(k, v)

    def register(self, k: str, v):
        if isinstance(v, Unit):
            self.units[k] = v
            for n in v.names:
                self.units[n] = v
            for n in v.symbols:
                self.units[n] = v
        elif isinstance(v, Dimension):
            self.dimensions[k] = v
        elif isinstance(v, PrefixSet):
            self.prefix_sets[k] = v
            for prefix in v:
                self._prefixes[prefix.prefix] = prefix
                self._prefixes[prefix.symbol] = prefix

    def get(self, name: str):
        if name in self.dimensions:
            return self.dimensions[name]

        if name in self.prefix_sets:
            return self.prefix_sets[name]

        if name in self.units:
            return self.units[name]

        for p, prefix in self._prefixes.items():
            if not name.startswith(p):
                continue
            unit_name = name.removeprefix(p)
            if unit_name not in self.units:
                continue
            unit = self.units[unit_name]
            if not prefix in unit.prefixes:
                if not conf.get('units_all_prefixes'):
                    continue
            return prefix.value * unit

        raise NameError(
            f'No unit (or prefixed unit)'
            f' with name {name!r} could be found.')

    def __getitem__(self, name: str):
        return self.get(name)

    @property
    def all_units(self):
        units: dict[str, Unit] = {}

        for name, unit in self.units.items():
            units[name] = unit
            units[unit.name] = unit
            units[unit.symbol] = unit

            for prefix in unit.prefixes:
                prefix: Prefix
                units[prefix.prefix + unit.name] = unit * prefix.value
                units[prefix.symbol + unit.symbol] = unit * prefix.value
        return units

    @property
    def prefixes(self):
        for prefix_set in self.prefix_sets.values():
            yield from prefix_set

    def __repr__(self):
        D = len(set(self.dimensions.values()))
        U = len(set(self.units.values()))
        S = len(list(self.prefix_sets.values()))
        P = len(list(self.prefixes))

        return (
            f'<Catalogue: {D} dimensions,'
            f' {U} units, {S} sets of {P} prefixes>')

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
                    set(self.units.values()),
                    key=lambda u: u.name
                )
            ]
        }
