"""Noether: Mathematical and scientific constants"""

# pylint: disable=W0401,W0614,W0611,C0103

from math import pi

from .scale import prefix
from .unit import Unit, BaseUnit, Dimension  # noqa: F401
from .unitCatalogue import *

# Trigonometry

tau = pi * 2
turn = cirle = tau * radian

# Quantum

h = BaseUnit(6.626_070_15e-34 * joule * second, "h")
hbar = BaseUnit(h / tau, "ħ")

# Electromagnetic

c = BaseUnit(299_792_458 * metre / second, "c")
Lightsecond = BaseUnit(c * second, "ls")
Lightyear = BaseUnit(c * year, "ly")

Permeability = force / current ** 2
mu_0 = BaseUnit(2 * tau * 1e-7 * newton / ampere ** 2)

Permittivity = 1 / (Permeability * speed ** 2)
e_0 = BaseUnit(1 / (mu_0 * c ** 2))

Impedance = Permeability * speed
z_0 = BaseUnit(mu_0 * c)

# Other fields
grav = BaseUnit(6.674_08e-11 * newton * metre ** 2 / kilogram ** 2)
k_e = BaseUnit(1 / (2 * tau * e_0))

# Material

n_a = 6.022_140_76e23 / mole

k_B = BaseUnit(1.380649e-23 * joule / kelvin, 'k_b')
R = n_a * k_B

# Atomic

e = BaseUnit(1.602_176_634e-19 * coulomb, "e")
m_e = BaseUnit(9.109_383_56e-31 * kilogram, "mₑ")

alpha = k_e * e ** 2 / (hbar * c)

r_e = (k_e * e ** 2) / (m_e * c ** 2)
rydberg = (m_e * e ** 4) / (8 * e_0 ** 2 * h ** 3 * c)

# Naturalised units

eV = BaseUnit(e * volt, "eV")
MeV = BaseUnit(prefix.M * eV, "MeV")
MeVc = BaseUnit(MeV / c, "MeVc⁻¹")
MeVc2 = BaseUnit(MeVc / c, "MeVc⁻²")

# Adopted values

g = gee / kilogram
t = 273.15 * kelvin

natural_units = (e_0, c, h, e, MeV, MeVc, MeVc2, grav)
