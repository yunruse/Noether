'''
Essential scientific units.
'''

from datetime import timedelta
from noether.core import Unit

from ..prefixes import SI_all
from ..fundamental import candela, kilogram, meter, second, kelvin
from math import pi
from .si import standard_gravity as g, c
from .si import minute, hour
from .si import year_julian as year  # <- This is the convention


# % Units of length
astronomical_unit = au = Unit(
    meter(149_597_870_700),
    "astronomical_unit", "au",
    info="conventional unit defined by the IAU in 2012"
)
parsec = Unit(au * 180*60*60/pi, "parsec", "pc", SI_all)

lightsecond = Unit(c * second, "lightsecond", "ls", SI_all)
lightyear = ly = Unit(c * year, "lightyear", "ly", SI_all)


# % Earth-sol system

lunation = synodic_month = Unit(
    timedelta(days=29, hours=12, minutes=44, seconds=2.9),
    ["lunation", "synodic_month"],
    info="Moon's average orbit with respect to the sol-earth line."
    " Moon phases are separated by a period close to this."
)
saros = Unit(
    lunation * 223, "saros",
    info="One saros after an eclipse, another occurs with similar geometry.")
sar = Unit(
    saros / 2, "sar",
    info="Half of a saros. One sar after a lunar eclipse, a solar eclipse occurs, and vice versa."
)


# % Solar system

sol = Unit(hour*24 + minute*39 + second*35.244, "sol",
           info="Mars' average day length")
