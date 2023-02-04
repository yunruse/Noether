'''
Essential scientific units.
'''

from ...core import Unit
from ...core.Prefix import SI

from ...core.fundamental import candela, kilogram, meter, second, kelvin
from math import pi
from .si import joule, watt, pascal, cumec, standard_gravity as g, c
from .cgs import cm
from .si import minute, hour
from .si import year_julian as year  # <- This is the convention


# % Astronomical
astronomical_unit = au = Unit(
    meter(149_597_870_700),
    "astronomical_unit", "au",
    info="conventional unit defined by the IAU in 2012"
)
parsec = Unit(au * 180*60*60/pi, "parsec", "pc", SI)

lightsecond = Unit(c * second, "lightsecond", "ls", SI)
lightyear = ly = Unit(c * year_julian, "lightyear", "ly", SI)

sol = Unit(hour*24 + minute*39 + second*35.244, "sol",
           info="Mars' average day length")
