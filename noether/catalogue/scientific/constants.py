'''
Mathematical and scientific constants not defined by SI or CODATA.
'''

from noether.core import Unit

from ..fundamental import ampere, kelvin, kilogram, meter
from .si import joule, newton, e, hbar, c
from .CODATA import CODATA

from math import pi

mu_0 = Unit(4 * pi * 1e-7 * newton / ampere ** 2, "mu_0", "μ₀")
e_0 = Unit(1 / (mu_0 * c ** 2), "e_0", "e₀")
z_0 = Unit(mu_0 * c, "z_0", "z₀")

k_e = Unit(1 / (4*pi*e_0), "k_e", "kₑ")

fine_structure_constant = alpha = Unit(
    k_e * e**2 / (hbar*c),
    ["fine_structure_constant", "alpha"], "α")
rydberg = Ry = Unit(
    joule(2.179_872_361_1035, 4.2e-15),
    "rydberg", "Ry", info="CODATA 2018")

# % Miscelleneous
t = kelvin(273.15)
water_density = (kilogram/meter**2)(0.9998395)
