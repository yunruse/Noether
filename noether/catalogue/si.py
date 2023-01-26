from ..core import Unit
from ..core.prefixes import SI, SI_small
from ..core.DisplaySet import display as I

from math import pi
from ..core.fundamental import *
from .dimensions import *

becquerel = Bq = Unit(frequency, 'becquerel', "Bq", SI)
hertz = Hz = I(Unit(frequency, 'hertz', "Hz", SI))

radian = rad = I(Unit(angle, 'radian', "rad", SI_small))
steradian = sr = I(Unit(solid_angle, 'steradian', "sr", SI))

# % Dynamics

newton = N = I(Unit(force, 'newton', "N", SI))
pascal = Pa = I(Unit(pressure, 'pascal', "Pa", SI))
joule = J = I(Unit(energy, 'joule', "J", SI))
watt = W = I(Unit(power, 'watt', "W", SI))

# % Electromagnetism

coulomb = C = I(Unit(charge, 'coulomb', "C", SI))
volt = V = I(Unit(voltage, 'volt', "V", SI))
farad = F = I(Unit(capacitance, 'farad', "F", SI))
ohm = Ω = I(Unit(resistance, 'ohm', "Ω", SI))
siemens = S = I(Unit(conductance, 'siemens', "S", SI))
henry = H = I(Unit(inductance, 'henry', "H", SI))
weber = Wb = I(Unit(magnetic_flux, 'weber', "Wb", SI))
tesla = T = I(Unit(magnetic_flux_density, 'tesla', "T", SI))

# % Radiation

lumen = lm = I(Unit(luminous_flux, 'lumen', "lm", SI))
lux = Lx = I(Unit(illuminance, 'lux', "Lx", SI))
gray = Gy = I(Unit(dose, 'gray', "Gy", SI))
sievert = Sv = I(Unit(dose, 'sievert', "Sv", SI))

# % Material properties

cumec = I(Unit(flow, 'cumec', None, SI))
katal = kat = I(Unit(catalytic_activity, 'katal', "kat", SI))


# % Constants defined as part of SI

# GCWM 3
standard_gravity = g = Unit(
    9.980665 * meter / second**2,
    "standard_gravity", "g")

# GCWM 17
speed_of_light = c = Unit(299_792_458 * meter / second, "c", "c")

# GCWM 26 (2019 redefinition of the SI base units)
electron_charge = e = Unit(
    coulomb(1.602_176_634e-19), "electron_charge", "e")
N_a = 6.022_140_76e23 / mole
boltzmann_constant = k_B = Unit(
    1.380649e-23 * joule / kelvin,
    "boltzmann_constant", 'k_b')
h = Unit(6.626_070_15e-34 * joule * second, "h", "h")
hbar = Unit(h / (pi*2), "hbar", "ħ")


eV = electronvolt = Unit(electron_charge * volt, "electronvolt", "eV", SI)
gee = g * kilogram
