'''
Mathematical and scientific constants.
'''

from ..core import Unit

from ..core.fundamental import ampere, kelvin, kilogram, meter
from .si import joule, newton, e, hbar, c
from math import pi

# % Electromagnetic

mu_0 = Unit(4 * pi * 1e-7 * newton / ampere ** 2, "mu_0", "μ₀")
e_0 = Unit(1 / (mu_0 * c ** 2), "e_0", "e₀")
z_0 = Unit(mu_0 * c, "z_0", "z₀")

k_e = Unit(1 / (4*pi*e_0), "k_e", "kₑ")
wien_displacement_constant = Unit(
    meter * kelvin * 2.897_771_955e-3,
    "wien_displacement_constant", "b")  # CODATA 2018 (fixed by definition)

# % Gravity
G = Unit(
    (newton * meter**2 / kilogram**2)(
        6.674_30e-11, 0.000_15e-11),
    "G", "G")  # CODATA 2018

# % Material
loschmidt_constant = n_0 = Unit(
    2.686_780_111e25 / meter**3,  # CODATA 2018 (fixed by definition)
    "loschmidt_constant", "n_0")

# % Atomic

atomic_mass_constant = m_u = Unit(
    kilogram(1.660_539_066_60e-27, 5e-37),
    "atomic_mass_constant", "m_u")  # CODATA 2018
electron_mass = m_e = Unit(
    kilogram(9.109_383_7015, 0.000_000_0028),
    "electron_mass", "m_e")  # CODATA 2018
fine_structure_constant = alpha = Unit(
    k_e * e**2 / (hbar*c),
    ["fine_structure_constant", "alpha"], "α")
rydberg_constant = Unit(
    # (m_e * e**4) / (8 * e_0**2 * h**3 * c),
    (1/meter)(10_973_731.568_160, 0.000_021),  # CODATA 2018
    "rydberg_constant", "R∞")
rydberg = Ry = Unit(
    # rydberg_constant * h * c,
    joule(2.179_872_361_1035, 4.2e-15),  #  CODATA 2018
    "rydberg", "Ry")

# % Naturalised units

# % Miscelleneous
t = kelvin(273.15)
water_density = (kilogram/meter**2)(0.9998395)
