'''
Historic CGS (centimeter-gram-second) unit system.
'''

from ...core import Unit
from ...core.fundamental import second as s, gram
from ..conventional import cm

from ..scientific import nit

gal = Unit(cm/s**2, "gal", "Gal")
dyne = Unit(gal * gram, "dyne", "dyn")
erg = Unit(dyne * s, "erg")
barye = Unit(gram / (cm * s**2), "barye", "Ba")
poise = Unit(gram / (cm*s), "poise", "P")
stokes = Unit(cm**2/s, "stokes", "St")
kayser = Unit(1/cm, "kayser", "K")

stilb = Unit(nit * 1e4, 'stilb', 'sb')


# TODO: Buckingham