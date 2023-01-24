'''
Mathematical and scientific constants.
'''

from ..core import Unit
from ..core.prefixes import SI, SI_small
from ..core.DisplaySet import display as I

from ..core.fundamental import ampere, kelvin, kilogram, meter, mole, second
from .si import SI, coulomb, joule, newton, radian, volt
from math import pi

# % Quantum

h = Unit(6.626_070_15e-34 * joule * second, "h", "h")  # GCWM 26
hbar = Unit(h / (pi*2), "hbar", "ħ")

# % Electromagnetic

c = Unit(299_792_458 * meter / second, "c", "c")  # GCWM 17

mu_0 = Unit(4 * pi * 1e-7 * newton / ampere ** 2, "mu_0", "μ₀")
e_0 = Unit(1 / (mu_0 * c ** 2), "e_0", "e₀")
z_0 = Unit(mu_0 * c, "z_0", "z₀")

k_e = Unit(1 / (4*pi*e_0), "k_e", "kₑ")

# % Gravity
G = Unit(
    (newton * meter**2 / kilogram**2)(
        6.674_30e-11, 0.000_15e-11),
    "G", "G")  # CODATA 2018
standard_gravity = g = Unit(
    9.980665 * meter / second**2,
    "standard_gravity", "g")  # GCWM 3
gee = g * kilogram

# % Material

N_a = 6.022_140_76e23 / mole  # GCWM 26
boltzmann_constant = k_B = Unit(
    1.380649e-23 * joule / kelvin,  # GCWM 26
    "boltzmann_constant", 'k_b')
loschmidt_constant = n_0 = Unit(
    2.686_780_111e25 / meter**3,  # CODATA 2018 (fixed by definition)
    "loschmidt_constant", "n_0")

# % Atomic

electron_charge = e = Unit(
    coulomb(1.602_176_634e-19), "electron_charge", "e")  # GCWM 26
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
eV = electronvolt = Unit(electron_charge * volt, "electronvolt", "eV", SI)

# % Miscelleneous
t = kelvin(273.15)
water_density = (kilogram/meter**2)(0.9998395)
