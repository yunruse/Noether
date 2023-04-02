'''
Essential scientific units.
'''

from noether.core import Unit

from math import pi

from ..prefixes import SI_all, micro
from ..fundamental import candela, kilogram, meter, kelvin, ampere
from .si import radian, steradian
from .si import joule, watt, pascal, cumec
from .si import hour

# % Angle
gradian = Unit(radian * pi / 200, "gradian", "grad")
circle = turn = Unit(radian * 2*pi, "turn", "turn")
sphere = spat = Unit(steradian * 4*pi, "spat", "sp")

# % Electricity
watt_hour = Wh = Unit(watt * hour, 'watt_hour', 'Wh', SI_all)
amp_hour = ampere_hour = Ah = Unit(ampere * hour, 'amp_hour', 'Ah', SI_all)
ampere_turn = At = Unit(ampere * turn, "ampere_turn", "At", SI_all)

# % Human
small_calorie = cal = Unit(
    4.814 * joule, ["calorie", "large_calorie"], "cal",
    info="Energy to heat 1g of water by 1°C."
    " Defined by convention; now regarded as obsolete."
    " Not to be confused with the large calorie (heats 1kg)."
)
large_calorie = kilocalorie = kcal = Unit(
    cal * 1000, ["kilocalorie", "small_calorie"], "kcal",
    info="Energy to heat 1kg of water by 1°C."
    " Defined by convention; now regarded as obsolete."
    " Not to be confused with the small calorie (heats 1g)."
    " Often used in food as an alternative to the kilojoule."
)
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

bar = Unit(1e5 * pascal, "bar", "bar", SI_all)
atmosphere = atm = Unit(101_325 * pascal, "atmosphere", ["atm", "ata"])
metre_mercury = meter_mercury = Unit(
    pascal(133_322.387_415),
    "meter_mercury", "mHg", SI_all,
    info="defined by convention")
mercury = meter_mercury / meter
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

micron = micro * meter
angstrom = Unit(meter(1e-10), "angstrom", "Å")
barn = Unit(1e-28 * meter**2, "barn", "b", SI_all)

# % Photometric
nit = Unit(candela / meter**2, 'nit', 'nit')
