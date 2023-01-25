'''
Imperial units.
'''

from fractions import Fraction

from ..core import Unit
from ..core.config import Config, conf

from .conventional import cm, liter


Config.register('imperial_country', 'us', '''\
Either `us` or `uk`, used to define imperial units.
(Both are available with the _us and _uk suffixes.)
''')

_USE_US_UNITS = conf.get('imperial_country').lower() == 'us'


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


# % Area

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
