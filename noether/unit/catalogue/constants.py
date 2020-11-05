"""Noether: Mathematical and scientific constants"""

from fractions import Fraction as F

from math import pi

from ...helpers import sqrt

from ..unit import Unit

from .fundamental import ampere, kelvin, kilogram, metre, mole, second
from .si import SI, coulomb, joule, newton, radian, volt
from .conventional import cm

# # Quantum

h = Unit(6.626_070_15e-34 * joule * second, "h")
hbar = Unit(h / (pi*2), "ħ")

# # Electromagnetic

c = Unit(299_792_458 * metre / second, "c")

mu_0 = Unit(4 * pi * 1e-7 * newton / ampere ** 2)  # permeability
e_0 = Unit(1 / (mu_0 * c ** 2))  # permittiviity
z_0 = Unit(mu_0 * c)  # impedance

# # Other fields
G = grav = (newton * metre**2 / kilogram**2)(6.674_30e-11, 0.00015e-11)
k_e = Unit(1 / (4 * pi * e_0))

# # Material

N_a = 6.022_140_76e23 / mole

k_B = Unit(1.380649e-23 * joule / kelvin, 'k_b')
R = N_a * k_B

# # Atomic

e = Unit(1.602_176_634e-19 * coulomb, "e")
m_e = Unit(9.109_383_56e-31 * kilogram, "m_e")

alpha = k_e * e ** 2 / (hbar * c)

r_e = (k_e * e ** 2) / (m_e * c ** 2)
rydberg = (m_e * e ** 4) / (8 * e_0 ** 2 * h ** 3 * c)

# # Naturalised units

eV = SI(e * volt, "eV")
MeV = Unit(1e6 * eV, "MeV")
MeVc = Unit(MeV / c, "MeVc⁻¹")
MeVc2 = Unit(MeVc / c, "MeVc⁻²")

# # Adopted values

g = 9.980665 * metre / second**2
gee = g * kilogram
t = 273.15 * kelvin

natural_units = (e_0, c, h, e, MeV, MeVc, MeVc2, grav)

# # Estimations of body surface area

# Sardinha et al, 2006. https://doi.org/10.1088/0967-3334/27/11/01
du_bois_index = 0.007184 / kilogram**F(17/40) * cm**F(29/40)
# Mosteller, 1987. https://doi.org/10.1056/NEJM198710223171717
mosteller_index = sqrt(1/3600) / (kilogram*cm) ** F(1/2)
