'''
Automatically-loaded CODATA fundamental physical constants.
'''

from ..core import Unit
from ..config import Config, conf

from ..core.Catalogue import Catalogue

from . import si
catalogue = Catalogue(vars(si))


def scanline(string: str, lengths: list[int]) -> list[str]:
    chunks = []
    for N in lengths:
        chunks.append(string[:N].strip())
        string = string[N:]
    return chunks + [string.strip()]


LENGTHS = [60, 25, 25]
NAMED_CODATA_UNITS = {
    'atomic mass constant': 'u',
    'electron mass': 'm_e',
    'Newtonian constant of gravitation': 'G'
}

one = Unit(1)


def _fmt_value(string: str):
    if string == '(exact)':
        return 0
    return float(string
                 .replace(' ', '_')
                 .replace('...', '')
                 .replace('_e', 'e')
                 )


def _codata(path: str):
    units:  dict[str, Unit] = dict()

    scanning = False
    with open(path) as f:
        for line in f.readlines():
            if not scanning:
                scanning = line.startswith('----')
                continue

            name, value, uncertainty, unit = scanline(line, LENGTHS)

            chunks = name.split()
            if 'in' in chunks and not name.startswith('shielding'):
                continue  # already defined in another unit
            if chunks[-1] == 'relationship':
                continue  # unit does not need extra definition

            value = _fmt_value(value)
            uncertainty = _fmt_value(uncertainty) or None
            unit = unit.replace('^', '**').replace(' ', '*')
            unit = eval(unit, {}, catalogue) if unit else one

            symbol = NAMED_CODATA_UNITS.get(name)
            units[name] = Unit(
                unit(value, uncertainty),
                name,
                symbol,
                info='CODATA 2018',
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
    nice_name = (
        name.replace(' ', '_')
            .replace('-', ' ')
            .replace('._', '_')
            .replace('.', '_')
            .replace('_(', '_with_')
            .replace(')', '')
            .replace(',', '')
            .replace('/', '_over_')
        # other stuff also?
    )
    locals()[nice_name] = unit
    __all__.append(nice_name)

    if unit.symbols:
        locals()[unit.symbol] = unit
        __all__.append(unit.symbol)
