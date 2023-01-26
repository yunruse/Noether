from ..core import Unit
from ..core.prefixes import SI, SI_small
from ..core.DisplaySet import display as I

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
