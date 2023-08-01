'''
Avourdupois, US customary and British imperial units.
'''

# TODO: #1 all of this nonsense

from fractions import Fraction

from noether.core import Unit, AffineUnit
from noether.config import Config, conf

from ..scientific import meter, kelvin, second, lumen
from ..scientific import cm, gram, hour
from ..scientific import standard_gravity, mercury
from .conventional import liter, msw

# TODO: change this system for gnu's br- prefix for british units?

USE_CUSTOMARY = Config.register('UNITS_customary', True, '''\
Define ambiguous imperial units (gallon, etc) using US Customary units instead of UK imperial units.
''')

_US = conf.get(USE_CUSTOMARY)

rankine = Unit(kelvin * 5/9, "rankine", "°R")
fahrenheit = degF = AffineUnit(rankine, rankine(459.67), "fahrenheit", "°F")

# % Length
inch = Unit(cm * Fraction(127, 50), "inch", ["in", '"'])

barleycorn = Unit(inch / 3, "barleycorn")
thou = Unit(inch / 1000, "thou")
twip = Unit(inch / 1440, "twip")  # twentieth of a point

# twip =
hand = Unit(inch * 4, "hand", "hh")
foot = Unit(inch * 12, "foot", ["ft", "'"])
yard = Unit(foot * 3, "yard", "yd")
chain = Unit(yard * 22, "chain", "ch")
furlong = Unit(chain * 10, "furlong", "fur")
mile = Unit(furlong * 8, "mile", "mi")
league = Unit(mile * 3, "league", "lea")
# TODO: maritime units, Gunter's survey units

# % Speed
nautical_mile = Unit(meter * 1852, "nautical_mile", "nmi")

mph = miles_per_hour = Unit(mile / hour, "miles_per_hour", "mph")
knot = Unit(nautical_mile / hour, "knot", ["kn", "kt"])


# % Area

acre = Unit(chain * furlong, "acre", "ac")

# TODO: all of this nonsense
# TODO: convert to new .yaml system
# and include:
# - https://en.wikipedia.org/wiki/Hundredweight
# - `quarter` thereof
# - poncelet

# % Volume
gallon_uk = gal_uk = Unit(liter(4.546_09), "gallon_uk", "gal")
quart_uk = Unit(gallon_uk / 4, "quart_uk", "qt")
pint_uk = Unit(gallon_uk / 8, "pint_uk", "pt")
fluid_ounce_uk = floz_uk = Unit(pint_uk / 20, "fluid_ounce_uk", "fl oz")
dram_uk = Unit(floz_uk / 8, "dram_uk", "dr")
gill_uk = Unit(floz_uk * 5, "gill_uk")

gallon_us = gal_us = Unit(inch**3 * 231, "gallon_us", "gal")
quart_us = Unit(gallon_us / 4, "quart_us", "qt")
pint_us = Unit(gallon_us / 8, "pint_us", "pt")
fluid_ounce_us = floz_us = Unit(pint_us / 16, "fluid_ounce_us", "fl oz")
dram_us = Unit(floz_us / 8, "dram_us", "dr")
gill_us = Unit(floz_us * 4, "gill_us")

gallon = gallon_us if _US else gallon_uk
pint = pint_us if _US else pint_uk
fluid_ounce = floz = floz_us if _US else floz_uk
dram = dram_us if _US else dram_uk
quart = quart_us if _US else quart_uk
gill = gill_us if _US else gill_uk

# gallon_us_dry = usdrygal = Unit(bushel_us / 8, "gallon_us_dry", "usdrygal"))

hogshead = Unit(66 * gallon_uk, "hogshead", "hhd")  # TODO
butt = Unit(hogshead * 2, "butt")  # y'all nerds


# % Mass
pound = lb = Unit(453.59237 * gram, "pound", "lb")
stone = st = Unit(pound * 14, "stone", "st")
ounce = oz = Unit(pound / 16, "ounce", "oz")
dram = drachm = dr = Unit(ounce / 16, ["dram", "drachm"], ["dr", "ʒ"])

poundforce = lbf = Unit(pound * standard_gravity, "poundforce", "lbf")
poundal = Unit(lb * foot / second**2, "poundal", "pdl")
pound_foot = foot_pound = Unit(lbf * foot, "pound_foot", "lbft")
slug = Unit(lbf / (foot / second**2), "slug", "slug")

grain = Unit(pound / 7000, "grain", "gr")

imperial_ton = Unit(pound * 2240, "imperial_ton", "t", info="imperial")


# % Derived

pound_per_square_inch = psi = Unit(
    lbf / inch**2, "pound_per_square_inch", "psi")
fsw = Unit(msw * foot/meter, "foot_sea_water", "fsw")

inch_mercury = Unit(mercury * inch,
                    "inch_mercury", "inHg")

foot_candle = Unit(lumen / foot**2, "foot_candle", "fc")
