'''
Imperial units.
'''

from fractions import Fraction

from noether.core import Unit, AffineUnit
from noether.config import Config, conf

from ..scientific import meter, kelvin, mercury
from ..scientific import cm, gram, hour
from .conventional import liter

Config.register('UNITS_country', 'us', '''\
The country to define imperial units (and other niceties) from. (Use the ISO 3166 code.)
''')
_USE_US_UNITS = conf.get('UNITS_country').lower() == 'us'

rankine = Unit(kelvin * 5/9, "rankine", "°R")
fahrenheit = degF = AffineUnit(rankine, rankine(459.67), "fahrenheit", "°F")

# % Length
inch = Unit(cm * Fraction(127, 50), "inch", ["in", '"'])

barleycorn = Unit(inch / 3, "barleycorn")
thou = Unit(inch / 1000, "barleycorn")
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

# % Volume
gallon_uk = Unit(liter(4.546_09), "gallon_uk", "gal")
gallon_us = Unit(inch**3 * 231, "gallon_us", "gal")
# gallon_us_dry = usdrygal = Unit(bushel_us / 8, "gallon_us_dry", "usdrygal"))

pint_uk = Unit(gallon_uk / 8, "pint_uk", "pt")
pint_us = Unit(gallon_us / 8, "pint_us", "pt")
pint = pint_us if _USE_US_UNITS else pint_uk

fluid_ounce_uk = floz_uk = Unit(pint_uk / 12, "fluid_ounce_uk", "fl oz")
fluid_ounce_us = floz_us = Unit(pint_us / 16, "fluid_ounce_us", "fl oz")
fluid_ounce = floz = floz_us if _USE_US_UNITS else floz_uk


dram = Unit(fluid_ounce / 8, "dram", "dr")


hogshead = Unit(0, "hogshead", "hhd")  # TODO
butt = Unit(hogshead * 2, "butt")  # y'all nerds


# % Mass
pound = lb = Unit(453.59237 * gram, "pound", "lb")

oz = ounce = Unit(pound / 16, "ounce", "oz")
grain = Unit(pound / 7000, "grain", "gr")

stone = st = Unit(pound * 14, "stone", "st")
imperial_ton = Unit(pound * 2240, "ton", "t")


# Derived

inch_mercury = Unit(mercury * inch,
                    "inch_mercury", "inHg")
