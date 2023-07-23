'''
Obscure scientific units.
'''

from math import pi
from noether.core import Unit

from ..scientific.si import hertz
from ..scientific.essential import nit


# % Photometric units
fresnel = Unit(hertz(1e12), "fresnel")

apostlib = blondel = Unit(nit / pi, "apostlib", "asb")
skot = Unit(apostlib(1e-3), "skot", "sk")
bril = Unit(apostlib(1e-7), "bril")
lambert = Unit(apostlib(1e4), "lambert", "L")
# TODO: foot-lambert

# TODO: go over purple links :)
