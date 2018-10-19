'''Noether: Mathematical and scientific constants'''

from math import pi

from .scale import *
from .unit import Unit
from .unitCatalogue import *

tau = pi * 2
circle = tau * Radian

# Physical constants

c = Unit(299_792_458 * Metre / Second, 'c')
Lightsecond = Unit(c * Second, 'ls')
Lightyear = Unit(c * Year, 'ly')

grav = Unit(6.67408e-11 * Newton * Metre**2 / Kilogram**2, 'G')
h = Unit(6.626_070_040e-34 * Joule * Second, 'h')
hbar = Unit(h / tau, 'ħ')

mu_0 = 2 * tau * 1e-7 * Newton / Ampere ** 2
e_0  = 1 / (mu_0 * c**2)
z_0  = mu_0 * c
k_e  = 1 / (2 * tau * e_0)

# Particle + chemical constants
e = Unit(1.60217646e-19 * Coulomb, 'e')
m_e = Unit(9.109_383_56e-31 * Kilogram, 'mₑ')

r_e = (k_e * e**2) / (m_e * c**2)

n_a = 6.022_140_857e23 / Mole

# Naturalised units
eV = Unit(e * Volt, 'eV')
MeV = Unit(prefix.M * eV, 'MeV')
MeVc = Unit(MeV / c, 'MeVc⁻¹')
MeVc2 = Unit(MeVc/c, 'MeVc⁻²')

# Adopted values

g = 9.80665
atom = 101325
t = 273.15

natural_units = (c, e, MeV, MeVc, MeVc2, grav)
