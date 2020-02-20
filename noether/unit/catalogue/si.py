"""
SI-derived units.

While more dimensions are defined in `dimensions.py`, the top 'paragraph'
in each section is defined in the same order as their units here.
"""

from .fundamental import U, Dimension
from .dimensions import *

SI = lambda x, y: U(x, y, display=True, SI=True)
# rotation

hertz = SI(frequency, "Hz")
radian = SI(angle, "rad")

steradian = SI(solid_angle, "sterad")

# dynamics

newton = SI(force, "N")
pascal = SI(pressure, "Pa")
joule = SI(energy, "J")
watt = SI(power, "W")

# electromagnetism

coulomb = SI(charge, "C")
volt = SI(voltage, "V")
farad = SI(capacitance, "F")
ohm = SI(resistance, "Ω")
siemens = SI(conductance, "S")
henry = SI(inductance, "H")
weber = SI(magnetic_flux, "Wb")
tesla = SI(magnetic_flux_density, "T")

# radiation

lumen = SI(luminous_flux, "lum")
lux = SI(illuminance, "Lx")
gray = SI(dose, "Gy")
#sievert = SI(dose, "Sv")

#becquerel = SI(hertz, "Bq")

# material properties

cumec = U(flow)
katal = SI(catalytic_activity, "kat")

# thermal properties

thermal_conductance = power / temperature
thermal_conductivity = thermal_conductance * length / area
thermal_resistance = temperature / power
thermal_resistivity = thermal_resistance * length / area
