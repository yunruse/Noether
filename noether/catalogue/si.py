from ..core import Unit
from ..core.prefixes import SI
from ..core.DisplaySet import display as I

from ..core.fundamental import *
from .dimensions import *

becquerel = I(Unit(frequency, 'becquerel', "Bq", SI))
hertz = I(Unit(frequency, 'hertz', "Hz", SI))
radian = I(Unit(angle, 'radian', "rad", SI))

steradian = I(Unit(solid_angle, 'steradian', "sterad", SI))

# # Dynamics

newton = I(Unit(force, 'newton', "N", SI))
pascal = I(Unit(pressure, 'pascal', "Pa", SI))
joule = I(Unit(energy, 'joule', "J", SI))
watt = I(Unit(power, 'watt', "W", SI))

# # Electromagnetism

coulomb = I(Unit(charge, 'coulomb', "C", SI))
volt = I(Unit(voltage, 'volt', "V", SI))
farad = I(Unit(capacitance, 'farad', "F", SI))
ohm = I(Unit(resistance, 'ohm', "Ω", SI))
siemens = I(Unit(conductance, 'siemens', "S", SI))
henry = I(Unit(inductance, 'henry', "H", SI))
weber = I(Unit(magnetic_flux, 'weber', "Wb", SI))
tesla = I(Unit(magnetic_flux_density, 'tesla', "T", SI))

# # Radiation

lumen = I(Unit(luminous_flux, 'lumen', "lum", SI))
lux = I(Unit(illuminance, 'lux', "Lx", SI))
gray = I(Unit(dose, 'gray', "Gy", SI))
sievert = I(Unit(dose, 'sievert', "Sv", SI))

# # Material properties

cumec = I(Unit(flow, 'cumec', None, SI))
katal = I(Unit(catalytic_activity, 'katal', "kat", SI))
