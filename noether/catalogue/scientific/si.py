'''
SI-derived units, and constants used in defining the SI units.
'''

from noether.core import Unit, UnitSet
from noether.core import display
from math import pi

from ..prefixes import SI_all as SI_all, SI_small, SI_large
from ..fundamental import *
from ..dimensions import *

SI = UnitSet({candela, ampere, kelvin, kilogram, mole, meter, second})


def SI_d(unit: Unit):
    return display(SI(unit))


# Time
minute = Unit(second*60, 'minute', ['min'])
hour = Unit(minute * 60, 'hour', ['hr', 'h'])
day = Unit(hour * 24, "day", "d")
year_julian = Unit(
    day * 365.25,
    "year", ["yr", "ya"], SI_large,
    info="Julian calendar - assuming leap year every 400 years."
    " Superseded by Gregorian year.")

# Rotation
becquerel = Bq = SI(Unit(frequency, 'becquerel', "Bq", SI_all))
hertz = Hz = SI_d(Unit(frequency, 'hertz', "Hz", SI_all))
radian = rad = SI_d(Unit(angle, 'radian', "rad", SI_small))
steradian = sr = SI_d(Unit(solid_angle, 'steradian', "sr", SI_all))

# Dynamics
newton = N = SI_d(Unit(force, 'newton', "N", SI_all))
pascal = Pa = SI_d(Unit(pressure, 'pascal', "Pa", SI_all))
joule = J = SI_d(Unit(energy, 'joule', "J", SI_all))
watt = W = SI_d(Unit(power, 'watt', "W", SI_all))

# Electromagnetism
coulomb = C = SI_d(Unit(charge, 'coulomb', "C", SI_all))
volt = V = SI_d(Unit(voltage, 'volt', "V", SI_all))
farad = F = SI_d(Unit(capacitance, 'farad', "F", SI_all))
ohm = Ω = SI_d(Unit(resistance, 'ohm', "Ω", SI_all))
mho = siemens = S = SI_d(Unit(conductance, 'siemens', "S", SI_all))
henry = H = SI_d(Unit(inductance, 'henry', "H", SI_all))
weber = Wb = SI_d(Unit(magnetic_flux, 'weber', "Wb", SI_all))
tesla = T = SI_d(Unit(magnetic_flux_density, 'tesla', "T", SI_all))

# Radiation
lumen = lm = SI_d(Unit(luminous_flux, 'lumen', "lm", SI_all))
lux = Lx = SI_d(Unit(illuminance, 'lux', "Lx", SI_all))
gray = Gy = SI_d(Unit(dose, 'gray', "Gy", SI_all))
sievert = Sv = SI_d(Unit(dose, 'sievert', "Sv", SI_all))

# Material properties
cumec = SI_d(Unit(flow, 'cumec', None, SI_all))
katal = kat = SI_d(Unit(catalytic_activity, 'katal', "kat", SI_all))


# % Constants defined as part of SI

# GCWM 3
standard_gravity = Unit(
    9.980665 * meter / second**2,
    "standard_gravity", "g", info="defined by convention")

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


eV = electronvolt = Unit(electron_charge * volt, "electronvolt", "eV", SI_all)
gee = standard_gravity * kilogram
