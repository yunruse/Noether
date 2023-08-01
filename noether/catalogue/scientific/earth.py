"""
Earth science units.
"""

from noether.core import Unit

from .si import meter, kilogram, standard_gravity as g
from ..conventional import year
from .cgs import cm
from .misc import cal

# Atmosphere
langley = Unit(cal / cm**2, "langley", "Ly", info="Unit of solar radiation")

# Geology

bubnoff = Unit(meter / (year*1e6), "bubnoff", "B")
