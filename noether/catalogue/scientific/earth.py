"""
Earth science units.
"""

from noether.core import Unit

from .si import meter, second
from ..conventional import year
from .cgs import cm
from .misc import cal

# Gravity
eotvos = Unit(1e-9 / second**2, "eotvos", "E")

# Atmosphere
langley = Unit(cal / cm**2, "langley", "Ly", info="Unit of solar radiation")

# Geology
bubnoff = Unit(meter / (year*1e6), "bubnoff", "B")
