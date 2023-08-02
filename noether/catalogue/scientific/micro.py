'''
Small-scale, atomic and nuclear units
'''

from noether.core import Unit

from ..prefixes import SI_all, SI_large, micro
from ..fundamental import kilogram, meter, mole
from .si import joule
from ..conventional.conventional import hour
from .CODATA import n_0, N_a  # type: ignore

# % Chemical

amagat = Unit(
    n_0 / N_a, "amagat", "amg")

# % Hartree atomic units
# where hbar = a_0 = m_e = e = 1

hartree = Unit(
    joule(4.359_744_722_2071e-18, 8.5e-30),  # CODATA 2018
    "hartree", "Eₕ")
bohr_radius = a_0 = Unit(
    meter(5.291_772_109_03e-11, 8e-21),  # CODATA 2018
    "bohr_radius", "a_0")

# % Small-scale

atomic_mass_unit = amu = dalton = Unit(
    1.660_539_066_60e-27 * kilogram,  # CODATA 2018
    ['atomic_mass_unit', 'dalton'], ['amu', 'Da'], SI_large)

micron = micro * meter
angstrom = Unit(meter(1e-10), "angstrom", "Å")

# % Nuclear
barn = Unit(1e-28 * meter**2, "barn", "b", SI_all)
inhour = Unit(1 / hour, "InHour", ["ih", "inhr"])
