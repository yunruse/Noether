'''
Essential scientific units.
'''

from noether.core import Unit
from noether.core.Prefix import SI

from noether.core.fundamental import candela, kilogram, meter, second, kelvin, ampere
from math import pi
from .si import radian, steradian
from .si import joule, watt, pascal, cumec, c
from .si import hour, minute, year_julian

# % Angle
gradian = Unit(radian * pi / 200, "gon")
circle = turn = Unit(radian * 2*pi, "turn", "turn")
sphere = spat = Unit(steradian * 4*pi, "spat", "sp")

# % Electricity
watt_hour = Wh = Unit(watt * hour, 'watt_hour', 'Wh', SI)
amp_hour = ampere_hour = Ah = Unit(ampere * hour, 'amp_hour', 'Ah')
ampere_turn = At = Unit(ampere * turn, "ampere_turn", "At")

# % Human
calorie = cal = Unit(4.814 * joule, "calorie", "cal",
                     info="not to be confused with the kcal")
kilocalorie = kcal = Unit(cal * 1000, "kilocalorie", "kcal")
bmi = Unit(kilogram / meter**2, "BMI", "BMI")

# A unit of solar irradiation
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

# % Photometric
nit = Unit(candela / meter**2, 'nit', 'nit')
