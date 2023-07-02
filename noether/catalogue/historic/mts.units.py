'''
Metre-tonne-second units.

Similar in nature to SI and CGS,
used in France and the Soviet Union.

https://en.wikipedia.org/wiki/MTS_units
'''

from noether.core import Unit, UnitSet

from ..fundamental import meter as m, second as s
from ..conventional import tonne as t

stere = stère = 'st' = m**3
# MTS unit used in firewood measurement (Greek stereós, "solid")

sthene = sthène = sthéne = 'sn' = t*m/s**2
# MTS unit (Greek sthénos, "force")

pieze = pièze = 'pz' = sthene / m**2
# MTS unit

MTS = UnitSet({
    m,
    t,
    s,
    stere,
    sthene
})
