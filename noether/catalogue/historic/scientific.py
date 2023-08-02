'''
Obscure scientific units.
'''

from math import pi
from noether.core import Unit

from noether.core.units import AffineUnit

from noether.catalogue.prefixes import SI_all

from ..scientific import kilogram, hertz, kelvin, meter, coulomb
from ..scientific import becquerel, nit, candela
from ..scientific import dalton, electron_charge
from ..scientific import cm, gram, au
from ..conventional import liter, foot


# % Photometry
fresnel = Unit(hertz(1e12), "fresnel")

apostilb = blondel = Unit(nit / pi, "apostilb", "asb")
skot = Unit(apostilb(1e-3), "skot", "sk")
bril = Unit(apostilb(1e-7), "bril")
lambert = Unit(apostilb(1e4), "lambert", ["Lb", "L"], SI_all)
foot_lambert = Unit(candela / pi / foot**2, "foot_lambert", "fL")

# TODO: foot-lambert

# % Temperature

degN = degNewton = AffineUnit(
    kelvin * 100/33, kelvin*273.15, "degNewton", "°N")
degRe = Reamur = AffineUnit(
    kelvin*0.8, kelvin*273.15, "Réamur", "°Ré")
degDe = Delisle = AffineUnit(
    kelvin*-2/3, kelvin*373.15, "Delisle", "°De")
degRo = Romer = AffineUnit(
    kelvin * 40/21, kelvin * (273.15-7.5 * 40/21), "Rømer", "°Rø")

# % Radiation

curie = Unit(
    3.7e10 * becquerel, "curie", "Ci",
    info="Introduced in 1910. Discouraged for the becquerel")
rutherford = Unit(
    1e6 * becquerel, "rutherford", "Rd",
    info="Introduced in 1946. Discouraged for the becquerel since 1975")
roentgen = Unit(
    2.58 * coulomb / kilogram, ["roentgen", "röntgen"], "R",
    info="Adopted as international standard in 1928. Deprecated since roughly 1998")
mache = Unit(
    3.64e-10 * curie / liter, "Mache", "ME",
    info="Deprecated")

# % Atomic

thomson = Unit(
    dalton / electron_charge, "thomson", "Th",
    info="Deprecated since 2013")

# % Astronomy

siriometer = Unit(au * 1e6, "siriometer", "sir")
spat_length = Unit(meter * 1e12, "spat_length", "S")

# % Earth

technical_atmosphere = Unit(
    kilogram * gram / cm**2, "technical_atmosphere", "at",
    info="Deprecated")
