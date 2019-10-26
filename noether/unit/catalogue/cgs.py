"""CGS system of units."""

from .conventional import cm, gram, second

gal = cm / second**2
dyne = gram * gal
erg = dyne * cm
barye = gram / gal
poise = gram / (cm * second)
stokes = cm**2 / second
kayser = 1 / cm