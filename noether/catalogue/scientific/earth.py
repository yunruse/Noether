"""
Earth science units.
"""

from noether.core import Unit, LogarithmicUnit

from .si import meter, second
from ..conventional import year
from .cgs import cm
from .misc import cal
from .micro import micron

# Gravity
eotvos = Unit(1e-9 / second**2, "eotvos", "E")

# Atmosphere
langley = Unit(cal / cm**2, "langley", "Ly", info="Unit of solar radiation")

# Meteorology
dBZ = LogarithmicUnit(
    micron**3, 10, 'dBZ', 'dBZ',
    info="Logarithmic unit of reflectivity used to measure precipitation")

# Geology
bubnoff = Unit(meter / (year*1e6), "bubnoff", "B")
