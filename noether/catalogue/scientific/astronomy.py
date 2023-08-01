'''
Essential scientific units.
'''

from datetime import timedelta
from noether.core import Unit

from ..prefixes import SI_all
from ..fundamental import candela, kilogram, meter, second, kelvin
from math import pi
from .si import standard_gravity as g, c, watt
from .si import minute, hour
from .si import year_julian as year  # <- This is convention


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

lunation = lunar_month = synodic_month = Unit(
    timedelta(days=29, hours=12, minutes=44, seconds=2.9),
    ["lunation", "lunar_month", "synodic_month"],
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

_gm = meter**3 / second**2

solar_mass = Unit(
    (kilogram * 1e30)(1.988_47, 0.00007), "solar_mass", "M☉")
# IAU 2015 refers to https://arxiv.org/abs/1510.07674
solar_radius = Unit(
    meter * 6.957e8, "solar_radius", ["R☉", "R_sol"],
    info="defined by convention IAU 2015")
solar_irradiance = solar_constant = Unit(
    1361 * watt / meter**2, "solar_constant", ["S☉", "S_sol"],
    info="defined by convention IAU 2015")
solar_luminosity = Unit(
    3.828e26 * watt, "solar_luminosity", ["L☉", "L_sol"],
    info="defined by convention IAU 2015")
solar_temperature = Unit(
    5772 * kelvin, "solar_temperature", ["T☉", "T_sol"],
    info="defined by convention IAU 2015")
solar_mass_parameter = Unit(
    1.327_124_4e20 * _gm, "solar_mass_parameter", ["(GM)☉", "GM_sol"],
    info="defined by convention IAU 2015")

earth_radius_equatorial = Unit(
    6.3871e6 * meter, "earth_radius_equatorial", "R_eE",
    info="defined by convention IAU 2015")
earth_radius_polar = Unit(
    6.3568e6 * meter, "earth_radius_polar", "R_pE",
    info="defined by convention IAU 2015")
jupiter_radius_equatorial = Unit(
    7.1492e7 * meter, "jupiter_radius_equatorial", "R_eJ",
    info="defined by convention IAU 2015")
jupiter_radius_polar = Unit(
    6.6854e7 * meter, "jupiter_radius_polar", "R_pJ",
    info="defined by convention IAU 2015")
earth_mass_parameter = Unit(
    3.986_004e14 * _gm, "earth_mass_parameter", "GM_earth",
    info="defined by convention IAU 2015")
jupiter_mass_parameter = Unit(
    1.266_865_3e17 * _gm, "jupiter_mass_parameter", "GM_jupiter",
    info="defined by convention IAU 2015")

sol = Unit(hour*24 + minute*39 + second*35.244, "sol",
           info="Mars' average day length")
