from math import pi

from .units import *

tau = pi * 2
circle = tau * Radian

# Physical constants

c = 299_792_458 * Metre / Second
Lightsecond = c * Second
Lightyear = Unit(c * Year, 'ly')

grav = 6.67408e-11 * Newton * Metre**2 / Kilogram**2
h = 6.626_070_040e-34 * Joule * Second
hbar = h / tau

mu_0 = 2 * tau * 1e-7 * Newton / Ampere ** 2
e_0  = 1 / (mu_0 * c**2)
z_0  = mu_0 * c
k_e  = 1 / (2 * tau * e_0)

# Particle + chemical constants

e = 1.60217646e-19 * Coulomb
eV = electronvolt = e * Volt
eVm = eV/c**2

m_e = 9.109_383_56e-31 * Kilogram
m_p = 1.672_621_898e-27 * Kilogram

r_e = (k_e * e**2) / (m_e * c**2)

n_a = 6.022_140_857e23 / Mole

# Adopted values

g = 9.80665
atom = 101325
t = 273.15
