"""Noether: Mathematical and scientific constants"""

from fractions import Fraction as F

from math import pi

from ...helpers import sqrt

from ..scale import prefix
from ..unit import Unit

from .fundamental import ampere, kelvin, kilogram, metre, mole, second
from .si import coulomb, joule, newton, radian, volt
from .scientific import c, gee
from .conventional import cm


# Trigonometry

tau = pi * 2
turn = cirle = tau * radian

# Quantum

h = Unit(6.626_070_15e-34 * joule * second, "h")
hbar = Unit(h / tau, "ħ")

# Electromagnetic

mu_0 = Unit(2 * tau * 1e-7 * newton / ampere ** 2)  # permeability
e_0 = Unit(1 / (mu_0 * c ** 2))  # permittiviity
z_0 = Unit(mu_0 * c)  # impedance

# Other fields
grav = Unit(6.674_08e-11 * newton * metre ** 2 / kilogram ** 2)
k_e = Unit(1 / (2 * tau * e_0))

# Material

n_a = 6.022_140_76e23 / mole

k_B = Unit(1.380649e-23 * joule / kelvin, 'k_b')
R = n_a * k_B

# Atomic

e = Unit(1.602_176_634e-19 * coulomb, "e")
m_e = Unit(9.109_383_56e-31 * kilogram, "mₑ")

alpha = k_e * e ** 2 / (hbar * c)

r_e = (k_e * e ** 2) / (m_e * c ** 2)
rydberg = (m_e * e ** 4) / (8 * e_0 ** 2 * h ** 3 * c)

# Naturalised units

eV = Unit(e * volt, "eV")
MeV = Unit(prefix.M * eV, "MeV")
MeVc = Unit(MeV / c, "MeVc⁻¹")
MeVc2 = Unit(MeVc / c, "MeVc⁻²")

# Adopted values

g = gee / kilogram
t = 273.15 * kelvin

natural_units = (e_0, c, h, e, MeV, MeVc, MeVc2, grav)

# estimations of body surface area

# Sardinha et al, 2006. https://doi.org/10.1088/0967-3334/27/11/01 
du_bois_index = 0.007184 / kilogram**F(17/40) * cm**F(29/40)
# Mosteller, 1987. https://doi.org/10.1056/NEJM198710223171717
mosteller_index = sqrt(1/3600) / (kilogram*cm) ** F(1/2)