"""
Historic units.

Cardarelli, François (1998). Scientific Unit Conversion.
"""

from .fundamental import U
from .si import newton, watt
from .conventional import (
    cm, metre, litre,
    gram, kilogram,
    second, hour, hectare
)

# # Attic Greek ~ 0 BCE

pous = metre * 0.30856

spithane = pous * 3/4
dichas = spithane / 2
palestra = dichas / 2
condylos = palestra / 2
daktylos = condylos / 2

greek_cubit = pous * 2
bema = pous * 5
orguia = bema * 2.4
akaina = orguia * 1.5
amma = akaina * (6+(2/3))
plethron = amma * (1+(2/3))
stadion = plethron * 6
mile = stadion * 7.5

# # Roman ~ 0 CE

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

# # Old Dutch, as taken in Amsterdam

voet = metre * 0.2830594

duim = voet / 12
lijne = duim / 12

elle = voet * 2.5  # distance from armpit to tip of fingers
roede = voet * 13

morgen = hectare * 0.856_532

# # French

french_point = truchet = cm * 0.0188
ligne = french_point * 12
pouce = ligne * 12
pied = french_foot = pouce * 12
toise = pied * 6
perche = pied * 22
arpent = perche * 10
vergee = vergée = 25 * perche**2

pinte = litre * 0.9521

quade = pinte * 2
velte = quade * 4
quartaut = velte * 9
feuillete = quartaut * 2
muid = feuillete * 2

chopine = pinte / 2
demiard = chopine / 2
posson = demiard / 2
roquille = posson / 4

poncelet = U(watt * 980.665, "p")

# # Metre-tonne-second units

stère = stere = ster = U(metre**3, "st")
sthène = sthéne = sthene = funal = U(newton * 1000, "sn", SI=True)
pièze = pieze = U(sthène / metre**2, "pz")
