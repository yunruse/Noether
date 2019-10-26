"""Historic units according to François Cardarelli.

Cardarelli, François (1998). Scientific Unit Conversion.
"""

from .fundamental import U
from .conventional import (
    cm, metre, litre,
    gram, kilogram,
    second, hour
)

# Attic Greek

pous = metre * 0.30856

spithane = pous * 3/4
dichas = spithane / 2
palestra = dichas / 2
condylos = palestra / 2
daktylos = condylos / 2

cubit = pous * 2
bema = pous * 5
orguia = bema * 2.4
akaina = orguia * 1.5
amma = akaina * (6+(2/3))
plethron = amma * (1+(2/3))
stadion = plethron * 6
mile = stadion * 7.5

# Roman

digitus = metre * 0.0184
palmus = digitus * 4
palmipes = palmus * 5
gradus = palmipes * 2
passus = gradus * 2
decempeda = passus * 2
roman_mile = passus * 1000

uncia = digitus * 4/3
pes = palmus * 4
cubitus = palmus * 6
actus = decempeda * 12

# Old Dutch

voet = metre * 0.2830594

duim = voet / 12
lijne = duim / 12

elle = voet * 2.5
roede = voet * 13