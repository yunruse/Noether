'''
Essential scientific units.
'''

from ..core import Unit
from ..core.prefixes import SI

from ..core.fundamental import candela, kilogram, meter, second, kelvin
from math import pi
from .si import joule, watt, pascal, cumec, g, c
from .conventional import cm, year

# % Human

calorie = cal = Unit(4.814 * joule, "calorie", "cal",
                     info="not to be confused with the kcal")
kilocalorie = kcal = Unit(cal * 1000, "kilocalorie", "kcal")
bmi = Unit(kilogram / meter**2, "BMI", "BMI")

# A unit of solar irradiation
langley = Unit(cal / cm**2, "langley", "Ly")
met = Unit(
    38.2 * watt / meter**2, "met", "met",
    info='energy per surface area of average person at rest')

# Used for insulation
RSI = Unit(meter**2 * kelvin / watt, "RSI")
tog = Unit(RSI * 0.1, "tog")
clo = Unit(tog * 1.55, "clo")

# % Pressure

bar = Unit(1e5 * pascal, "bar", "bar", SI)
atmosphere = atm = Unit(101_325 * pascal, "atmosphere", ["atm", "ata"])
technical_atmosphere = Unit(
    kilogram * g / cm**2, "technical_atmosphere", "at")
metre_mercury = meter_mercury = Unit(
    pascal(133_322.387_415),
    "meter_mercury", "mHg", SI,
    info="defined by convention")
sverdrup = Unit(cumec * 1e6, "sverdrup", "Sv")

# % Hartree atomic units
# where hbar = a_0 = m_e = e = 1

hartree = Unit(
    joule(4.359_744_722_2071e-18, 8.5e-30),  # CODATA 2018
    "hartree", "Eₕ")
bohr_radius = a_0 = Unit(
    meter(5.291_772_109_03e-11, 8e-21),  # CODATA 2018
    "bohr_radius", "a_0")

# % Small-scale

micron = meter(1e-6)
angstrom = Unit(meter(1e-10), "angstrom", "Å")
barn = Unit(1e-28 * meter**2, "barn", "b", SI)

# % Astronomical
astronomical_unit = au = Unit(
    meter(149_597_870_700),
    "astronomical_unit", "au",
    info="conventional unit defined by the IAU in 2012"
)
parsec = Unit(au * 180*60*60/pi, "parsec", "pc", SI)

lightsecond = Unit(c * second, "lightsecond", "ls", SI)
lightyear = ly = Unit(c * year, "lightyear", "ly", SI)

# % Photometric
nit = Unit(candela / meter**2, 'nit', 'nit')
