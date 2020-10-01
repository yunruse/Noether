"""
SI-derived units.

While more dimensions are defined in `dimensions.py`, the top 'paragraph'
in each section is defined in the same order as their units here.
"""

from .fundamental import U, Dimension
from .dimensions import *


def SI(x, y): return U(x, y, display=True, SI=True)

# # Rotation


becquerel = SI(frequency, "Bq")
hertz = SI(frequency, "Hz")
radian = SI(angle, "rad")

steradian = SI(solid_angle, "sterad")

# # Dynamics

newton = SI(force, "N")
pascal = SI(pressure, "Pa")
joule = SI(energy, "J")
watt = SI(power, "W")

# # Electromagnetism

coulomb = SI(charge, "C")
volt = SI(voltage, "V")
farad = SI(capacitance, "F")
ohm = SI(resistance, "Ω")
siemens = SI(conductance, "S")
henry = SI(inductance, "H")
weber = SI(magnetic_flux, "Wb")
tesla = SI(magnetic_flux_density, "T")

# # Radiation

lumen = SI(luminous_flux, "lum")
lux = SI(illuminance, "Lx")
gray = SI(dose, "Gy")
sievert = SI(dose, "Sv")

# # Material properties

cumec = U(flow)
katal = SI(catalytic_activity, "kat")

# # Thermal properties

thermal_conductance = power / temperature
thermal_conductivity = thermal_conductance * length / area
thermal_resistance = temperature / power
thermal_resistivity = thermal_resistance * length / area
