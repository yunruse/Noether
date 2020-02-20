"""
Units typical to scientific contexts.
"""

from .fundamental import (
    U, metre, second, kilogram, candela
)
from .si import watt, joule, pascal, cumec
from .conventional import cm, year

mps = metre / second
c = U(299_792_458 * metre / second, "c")

g = 9.980665 * metre / second**2
gee = g * kilogram

# human
calorie = U(4.814 * joule, "cal", SI=True, display=False)
kilocalorie = kcal = U(calorie * 1000, "kcal")
langley = (calorie / cm**2)(41840)

bar = U(1e5 * pascal, "bar", SI=True, display=False)
atmosphere = atm = U(101_325 * pascal, "atm", display=False)
technical_atmosphere = U(kilogram*g/cm**2, "at", SI=True)
torr = U(atmosphere / 760, "torr")
metre_mercury = meter_mercury = U(133_322.387_415 * pascal, "mhg", SI=True)
sverdrup = U(cumec * 1e6, "Sv")
amagat = U(2.686_7811 / metre**3, 'Am', SI=True)

bmi = U(kilogram / metre**2, "BMI")
met = U(58.2 * watt / metre ** 2, 'met')

# small-scale
angstrom = U(metre * 1e-10, "å")

are = U((10 * metre)**2, "a")
barn = U(1e-28 * metre**2, "b")

dalton = U(1.660_538_86e-27 * kilogram, "u")

# astronomical
parsec = U(3.0857e16 * metre, "pc", SI=True)
au = U(1.495_878_707e11 * metre, "au")

lightsecond = U(c * second, "ls", SI=True)
lightyear = U(c * year, "ly", SI=True)

solar_mass = U(1.98802e30 * kilogram, "msol")
# this one's quite controversial.
# currently using Hubble Space Telescope.
# Friedman et al, 2019. https://doi.org/10.3847/1538-4357/ab2f73
hubble = (mps / parsec / 1000)(69.8, 1.9)
