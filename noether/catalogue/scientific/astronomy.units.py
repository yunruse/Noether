from noether.core import Unit, UnitSet

from ..fundamental import meter
from .si import watt, hertz, kilogram, kelvin
from .si import second, minute, hour, day, year_julian as y
from .si import c, pi

#% astronomical "Astronomical"
# Units used in space science.

astronomical_unit = "au" = meter * 149_597_870_700
# mean distance from Earth to Sun
# defined by: IAU in 2012

parsec = "pc" = au * 180 * 60 * 60 / pi
# member of: si

lightsecond = 'ls' = c * second
# member of: si

lightyear = 'ly' = c * y
# member of: si


jansky = 'Jy' = 1e-26 * watt / meter**2 / hertz
# used in radio astronomy
# dimension: spectral_flux_density, spectral_irradiance


#% earth_sol "Earth-sol system"
# part of: astronomical

lunation = lunation = lunar_month = synodic_month = \
    day*29 + hour*12 + minute*44 + second*2.9
# Average time between moon phases;
# mean orbital period wrt sol-earth line.

saros = lunation * 223
# One saros after an eclipse, another occurs
# with similar geometry. There are m
# wikipedia: Saros (astronomy)

sar = saros / 2
# Exactly one sar after a lunar eclipse, a solar eclipse occurs,
# and vice versa.
# wikipedia: Sar (astronomy)

exeligmos = saros * 3
# One exeligmos after an eclipse, another occurs
# with similar geometry. Due to sidereal motion,
# this occurs at nearly the exact same time of day.
# wikipedia: Exeligmos


# TODO: eclipse years, eclipse seasons

_gm = meter**3 / second**2

#% iau "International Astronomical Union"
# https://arxiv.org/abs/1510.07674


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
