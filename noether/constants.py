'''Noether: Mathematical and scientific constants'''

from math import pi

from .scale import prefix
from .unit import Unit, BaseUnit as U
from .unitCatalogue import (
    Kilogram, Metre, Second, Ampere, Mole, Radian,
    Year, Newton, Joule, Coulomb, Volt,
)

tau = pi * 2
circle = tau * Radian

# Physical constants

c = U(299_792_458 * Metre / Second, 'c')
Lightsecond = U(c * Second, 'ls')
Lightyear = U(c * Year, 'ly')

grav = U(
    6.67408e-11 * Newton * Metre**2 / Kilogram**2,
    m='strength of force of gravity')
h = U(6.626_070_040e-34 * Joule * Second, 'h')
hbar = U(h / tau, 'ħ')

mu_0 = U(
    2 * tau * 1e-7 * Newton / Ampere ** 2,
    m='magnetic permeability')
e_0  = U(
    1 / (mu_0 * c**2),
    m='electric permittivity')
z_0  = U(
    mu_0 * c,
    m='impedance of free space')
k_e  = U(
    1 / (2 * tau * e_0),
    m='strength of electronmagnetism')


# Particle + chemical constants
e = U(1.60217646e-19 * Coulomb, 'e')
m_e = U(9.109_383_56e-31 * Kilogram, 'mₑ')

alpha = k_e * e**2 / (hbar * c)

r_e = (k_e * e**2) / (m_e * c**2)

n_a = 6.022_140_857e23 / Mole

rydberg = (m_e * e**4) / (8 * e_0**2 * h**3 * c)

# Naturalised units
eV = U(e * Volt, 'eV')
MeV = U(prefix.M * eV, 'MeV')
MeVc = U(MeV / c, 'MeVc⁻¹')
MeVc2 = U(MeVc/c, 'MeVc⁻²')

# Adopted values

g = U(9.80665 * Metre / Second ** 2, 'g')
atom = 101325
t = 273.15

natural_units = (e_0, c, h, e, MeV, MeVc, MeVc2, grav)
