
from noether.core import Unit

from .si import kilogram, standard_gravity as g
from .cgs import cm
from .essential import cal

technical_atmosphere = Unit(
    kilogram * g / cm**2, "technical_atmosphere", "at")
langley = Unit(cal / cm**2, "langley", "Ly", info="Unit of solar radiation")
