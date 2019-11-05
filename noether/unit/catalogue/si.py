"""
SI-derived units.

While more dimensions are defined in `dimensions.py`, the top 'paragraph'
in each section is defined in the same order as their units here.
"""

from .fundamental import U, Dimension
from .dimensions import *

# rotation

hertz = U(frequency, "Hz", SI=True)
radian = U(angle, "rad", SI=True)

steradian = U(angle**2, "sterad", SI=True)

# dynamics

newton = U(force, "N", SI=True)
pascal = U(pressure, "Pa", SI=True)
joule = U(energy, "J", SI=True)
watt = U(power, "W", SI=True)

# electromagnetism

coulomb = U(charge, "C", SI=True)
volt = U(voltage, "V", SI=True)
farad = U(capacitance, "F", SI=True)
ohm = U(resistance, "Ω", SI=True)
siemens = U(conductance, "S", SI=True)
henry = U(inductance, "H", SI=True)
weber = U(magnetic_flux, "Wb", SI=True)
tesla = U(magnetic_flux_density, "T", SI=True)

# radiation

lumen = U(luminous_flux, "lum", SI=True)
lux = U(illuminance, "Lx", SI=True)
gray = U(dose, "Gy", SI=True)
#sievert = U(dose, "Sv", SI=True)

#becquerel = U(hertz, "Bq", SI=True)

# material properties

cumec = U(flow)
katal = U(catalytic_activity, "kat")

# thermal properties

thermal_conductance = power / temperature
thermal_conductivity = thermal_conductance * length / area
thermal_resistance = temperature / power
thermal_resistivity = thermal_resistance * length / area
