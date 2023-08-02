'''
Miscelaneous or human scientific units.
'''

from noether.core import Unit

from math import pi

from ..prefixes import SI_all
from ..fundamental import candela, kilogram, meter, kelvin, ampere
from .si import radian, steradian
from .si import joule, watt, pascal, cumec
from .si import hour, minute, second

# % Angle
gradian = grade = Unit(radian * pi / 200, "gradian", "grad")
turn = Unit(
    radian * 2*pi,
    ["circle", "turn", "revolution", "rev"], "turn")
sphere = spat = Unit(steradian * 4*pi, "spat", "sp")

rpm = Unit(turn / minute, "revolutions_per_minute", "rpm")
rps = Unit(turn / second, "revolutions_per_second", "rps")

# % Electricity
watt_hour = Wh = Unit(watt * hour, 'watt_hour', 'Wh', SI_all)
amp_hour = ampere_hour = Ah = Unit(ampere * hour, 'amp_hour', 'Ah', SI_all)
ampere_turn = At = Unit(ampere * turn, "ampere_turn", "At", SI_all)

# % Human
small_calorie = cal = Unit(
    4.814 * joule, ["calorie", "small_calorie"], "cal",
    info="Energy to heat 1g of water by 1°C."
    " Defined by convention; now regarded as obsolete."
    " Not to be confused with the large calorie (heats 1kg).")
large_calorie = kilocalorie = kcal = Unit(
    cal * 1000, ["kilocalorie", "large_calorie"], "kcal",
    info="Energy to heat 1kg of water by 1°C."
    " Defined by convention; now regarded as obsolete."
    " Not to be confused with the small calorie (heats 1g)."
    " Often used in food as an alternative to the kilojoule.")
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
torr = Unit(atm / 760, "torr", "Torr")
metre_mercury = meter_mercury = Unit(
    pascal(133_322.387_415),
    "meter_mercury", "mHg", SI_all,
    info="defined by convention")
mercury = hg = meter_mercury / meter
sverdrup = Unit(cumec * 1e6, "sverdrup", "Sv")

# % Photometric
nit = Unit(candela / meter**2, 'nit', 'nt', SI_all)
