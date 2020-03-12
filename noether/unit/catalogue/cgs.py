"""
Centimetre-gram-second (metric) system of units.
"""

from .fundamental import U
from .conventional import cm, gram, second

gal = galileo = U(cm / second**2, 'Gal', SI=True)
dyne = U(gram * gal, 'dyn', SI=True)
erg = U(dyne * cm, 'erg', SI=True)
barye = U(gram / gal, 'Ba', SI=True)
poise = U(gram / (cm * second), 'P', SI=True)
stokes = U(cm**2 / second, 'St', SI=True)
kayser = U(1 / cm, SI=True)
eotvos = U(1e-9 * gal / cm, 'E', SI=True)
