'''
Regional customary units.
Typically the most predominant unit is taken;
though 

'''

from ...core import Unit
from ...core.fundamental import meter
from ..conventional import hectare


# % Spanish customary units
# Unless specified, taken as Castillian value.

pie = pies = Unit(meter(0.2786), "pies")

pulgada = Unit(pie / 12, "pulgada")
linea = Unit(pulgada / 12, "pulgada")
punto = Unit(pie / 12, "pulgada")

# Taken by its Puerto Rican value.
spanish_acre = cuerda = Unit(meter(3_930.395_625), 'cuerda')

# Used by Spanish viceroyalties in the Americas.
caballeria = caballería = Unit(
    hectare(78.58),
    "caballería"
)