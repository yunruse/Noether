'''
Obscure or otherwise historic units.
'''

from math import pi
from ...core import Unit

from ..si import hertz
from ..scientific import nit


# % Photometric units
fresnel = Unit(hertz(1e12), "fresnel")

apostlib = blondel = Unit(nit / pi, "apostlib", "asb")
skot = Unit(apostlib(1e-3), "skot", "sk")
bril = Unit(apostlib(1e-7), "bril")
lambert = Unit(apostlib(1e4), "lambert", "L")
# TODO: foot-lambert

# TODO: go over purple links :)