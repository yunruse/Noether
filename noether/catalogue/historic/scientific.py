'''
Obscure scientific units.
'''

from math import pi
from noether.core import Unit

from noether.core.units import AffineUnit

from ..scientific import hertz, kelvin, becquerel, nit
from ..scientific import dalton, electron_charge


# % Photometric units
fresnel = Unit(hertz(1e12), "fresnel")

apostlib = blondel = Unit(nit / pi, "apostlib", "asb")
skot = Unit(apostlib(1e-3), "skot", "sk")
bril = Unit(apostlib(1e-7), "bril")
lambert = Unit(apostlib(1e4), "lambert", "L")

# TODO: foot-lambert

# % Temperature units

degN = degNewton = AffineUnit(
    kelvin * 100/33, kelvin*273.15, "degNewton", "°N")
degRe = Reamur = AffineUnit(
    kelvin*0.8, kelvin*273.15, "Réamur", "°Ré")
degDe = Delisle = AffineUnit(
    kelvin*-2/3, kelvin*373.15, "Delisle", "°De")
degRo = Romer = AffineUnit(
    kelvin * 40/21, kelvin * (273.15-7.5 * 40/21), "Rømer", "°Rø")

# % Radiation

curie = Unit(3.7e10 * becquerel, "curie", "Ci")
rutherford = Unit(1e6 * becquerel, "rutherford", "Rd")

# % Atomic

thomson = Unit(dalton / electron_charge, "thomson", "Th")
