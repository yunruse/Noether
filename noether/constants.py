"""Noether: Mathematical and scientific constants"""

# pylint: disable=W0401,W0614,W0611,C0103

from math import pi

from .scale import prefix
from .unit import Unit, BaseUnit, Dimension  # noqa: F401
from .unitCatalogue import *

# Trigonometry

tau = pi * 2
circle = tau * Radian

# Quantum

h = BaseUnit(6.626_070_15e-34 * Joule * Second, "h")
hbar = BaseUnit(h / tau, "ħ")

# Electromagnetic

c = BaseUnit(299_792_458 * Metre / Second, "c")
Lightsecond = BaseUnit(c * Second, "ls")
Lightyear = BaseUnit(c * Year, "ly")

Permeability = Force / Current ** 2
mu_0 = BaseUnit(2 * tau * 1e-7 * Newton / Ampere ** 2)

Permittivity = 1 / (Permeability * Speed ** 2)
e_0 = BaseUnit(1 / (mu_0 * c ** 2))

Impedance = Permeability * Speed
z_0 = BaseUnit(mu_0 * c)

# Other fields
grav = BaseUnit(6.674_08e-11 * Newton * Metre ** 2 / Kilogram ** 2)
k_e = BaseUnit(1 / (2 * tau * e_0))

# Material

n_a = 6.022_140_76e23 / Mole

k_B = BaseUnit(1.380649e-23 * Joule / Kelvin, 'k_b')
R = n_a * k_B

# Atomic

e = BaseUnit(1.602_176_634e-19 * Coulomb, "e")
m_e = BaseUnit(9.109_383_56e-31 * Kilogram, "mₑ")

alpha = k_e * e ** 2 / (hbar * c)

r_e = (k_e * e ** 2) / (m_e * c ** 2)
rydberg = (m_e * e ** 4) / (8 * e_0 ** 2 * h ** 3 * c)

# Naturalised units

eV = BaseUnit(e * Volt, "eV")
MeV = BaseUnit(prefix.M * eV, "MeV")
MeVc = BaseUnit(MeV / c, "MeVc⁻¹")
MeVc2 = BaseUnit(MeVc / c, "MeVc⁻²")

# Adopted values

g = BaseUnit(9.80665 * Metre / Second ** 2, "g")
t = 273.15 * Kelvin

natural_units = (e_0, c, h, e, MeV, MeVc, MeVc2, grav)

# Symbols

π = pi
τ = tau
ħ = hbar
α = alpha
μ = mu_0
ε = e_0
