from noether.core import Unit, UnitSet

from ..fundamental import meter as m, second as s
from ..conventional import tonne as t

#% mts "Meter-tonne-second system"
# Similar in nature to SI and CGS,
# used historically in France and the Soviet Union.
# wikipedia: https://en.wikipedia.org/wiki/MTS_units

m
t
s

stere = stère = 'st' = m**3
# used in firewood measurement
# etymology: Greek stereós, "solid"

sthene = sthène = sthéne = 'sn' = t*m/s**2
# etymology: Greek sthénos, "force"

pieze = pièze = 'pz' = sthene / m**2
