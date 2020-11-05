"""
Units typical to scientific contexts.
"""

from math import pi
from .fundamental import (
    U, metre, second, kilogram, candela
)
from .si import watt, joule, pascal, cumec
from .conventional import cm, year
from .constants import alpha, c, hbar, m_e, g

# # Human

mps = metre / second

calorie = U(4.814 * joule, "cal", SI=True, display=False)
kilocalorie = kcal = U(calorie * 1000, "kcal")
langley = (calorie / cm**2)(41840)

bmi = U(kilogram / metre**2, "BMI")
met = U(58.2 * watt / metre ** 2, 'met')

# # Atmospheric

bar = U(1e5 * pascal, "bar", SI=True, display=False)
atmosphere = atm = U(101_325 * pascal, "atm", display=False)
technical_atmosphere = U(kilogram*g/cm**2, "at", SI=True)
torr = U(atmosphere / 760, "torr")
metre_mercury = meter_mercury = U(133_322.387_415 * pascal, "mhg", SI=True)
sverdrup = U(cumec * 1e6, "Sv")
amagat = U(2.686_7811 / metre**3, 'Am', SI=True)

bmi = U(kilogram / metre**2, "BMI")
met = U(58.2 * watt / metre ** 2, 'met')

# # Hartree atomic units
# where hbar = a_0 = m_e = e = 1

hartree = U(joule * 4.359_744_722_2071e-18, "E_h")
bohr = a_0 = U(hbar / m_e / c / alpha, 'a_0')

# # Small-scale

# TODO: have "micron", "kilogram" etc understood as SI units but with prefixes
micron = U(metre * 1e-6, "µm")

angstrom = U(metre * 1e-10, "Å")

are = U((10 * metre)**2, "a")
barn = U(1e-28 * metre**2, "b")

dalton = U(1.660_538_86e-27 * kilogram, "u")

# # Astronomical
parsec = U(3.0857e16 * metre, "pc", SI=True)
au = U(1.495_878_707e11 * metre, "au")

lightsecond = U(c * second, "ls", SI=True)
lightyear = U(c * year, "ly", SI=True)

solar_mass = U(1.98802e30 * kilogram, "msol")
# this one's quite controversial.
# currently using Hubble Space Telescope.
# Friedman et al, 2019. https://doi.org/10.3847/1538-4357/ab2f73
hubble = (mps / parsec / 1000)(69.8, 1.9)

# # Photometric (incl. outdated)
fresnel = (1 / second)(1e12)

nit = U(candela / metre**2, 'nt')
stilb = U(candela / cm**2, 'sb')
apostilb = blondel = U(nit / pi, 'asb')
lambert = U(stilb / pi, 'L')
skot = U(apostilb / 1000, 'sk')
bril = U(skot / 10_000, 'bril')
