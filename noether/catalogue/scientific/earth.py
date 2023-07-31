"""
Earth science units.
"""

from noether.core import Unit

from .si import meter, kilogram, standard_gravity as g
from ..conventional import year
from .cgs import cm
from .essential import cal

# Atmosphere

technical_atmosphere = Unit(
    kilogram * g / cm**2, "technical_atmosphere", "at")
langley = Unit(cal / cm**2, "langley", "Ly", info="Unit of solar radiation")

# Geology

bubnoff = Unit(meter / (year*1e6), "bubnoff", "B")
