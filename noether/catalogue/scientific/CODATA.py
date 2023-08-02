'''
Automatically-loaded CODATA fundamental physical constants.
'''

from ...helpers import scanline
from noether.core import Unit
from ...config import Config, conf
from noether.core.Catalogue import Catalogue

from . import si
catalogue = Catalogue(vars(si), 'CODATA data-fetching catalogue')


COLUMN_LENGTHS = [60, 25, 25]
NAMED_CODATA_UNITS = {
    'atomic_mass_constant': 'u',
    'electron_mass': 'm_e',
    'Newtonian_constant_of_gravitation': 'G',
    'Loschmidt_constant_at_101_325_Pa': 'n_0',
    'Avogadro_constant': 'N_a',
    'Boltzmann_constant': 'k_B',
    'fine_structure_constant': 'α',
}

one = Unit(1)


def _fmt_name(string: str):
    return (string
            .replace(' ', '_')
            .replace('-', '_')
            .replace('._', '_')
            .replace('.', '_')
            .replace('_(', '_with_')
            .replace(')', '')
            .replace(',', '')
            .replace('/', '_over_')
            .replace('_with_273_15_K_', '_at_')
            .replace('101_325_kPa', '101_325_Pa')
            )


def _fmt_value(string: str):
    if string == '(exact)':
        return 0
    return float(string
                 .replace(' ', '_')
                 .replace('...', '')
                 .replace('_e', 'e')
                 )


def _codata(path: str):
    units: dict[str, Unit] = dict()

    scanning = False
    with open(path) as f:
        for line in f.readlines():
            if not scanning:
                scanning = line.startswith('----')
                continue

            full_name, value, uncertainty, unit = scanline(
                line, COLUMN_LENGTHS)

            # if full_name == 'Avogadro constant':
            #     # TODO: #42 ComposedUnit
            #     # HACK
            #     unit = ''

            chunks = full_name.split()
            if 'in' in chunks and not full_name.startswith('shielding'):
                continue  # already defined in another unit
            if chunks[-1] == 'relationship':
                continue  # unit does not need extra definition

            value = _fmt_value(value)
            name = _fmt_name(full_name)
            uncertainty = _fmt_value(uncertainty) or None
            unit = unit.replace('^', '**').replace(' ', '*')
            unit = eval(unit, {}, catalogue) if unit else one

            symbol = NAMED_CODATA_UNITS.get(name)
            units[name] = Unit(
                unit(value, uncertainty),
                name,
                symbol,
                info=f'{full_name}, CODATA 2018',
            )

    return units


_CODATA_PATH = __file__.removesuffix('.py') + '.txt'
CODATA = _codata(_CODATA_PATH)


Config.register('CATALOGUE_codata_all', True, '''\
Provide all CODATA constants in the Noether namespace,
such as `electron_mag_mom_to_nuclear_magneton_ratio`
''')

__all__ = ['CODATA']
for name, unit in CODATA.items():
    if not (conf.get('CATALOGUE_codata_all') or unit.name in NAMED_CODATA_UNITS):
        continue
    locals()[name] = unit
    __all__.append(name)

    if unit.symbols:
        locals()[unit.symbol] = unit
        __all__.append(unit.symbol)
