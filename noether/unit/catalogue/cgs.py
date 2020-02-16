"""CGS system of units."""

from .fundamental import U
from .conventional import cm, gram, second

# TODO: change `SI=` for clarity?
gal = U(cm / second**2, 'Gal', SI=True)
dyne = U(gram * gal, 'dyn', SI=True)
erg = U(dyne * cm, 'erg', SI=True)
barye = U(gram / gal, 'Ba', SI=True)
poise = U(gram / (cm * second), 'P', SI=True)
stokes = U(cm**2 / second, 'St', SI=True)
kayser = U(1 / cm, SI=True)
