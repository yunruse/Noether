"""
Centimetre-gram-second (metric) system of units.
"""

from .fundamental import U
from .conventional import cm, gram, second

gal = galileo = U(cm / second**2, 'Gal', si=True)
dyne = U(gram * gal, 'dyn', si=True)
erg = U(dyne * cm, 'erg', si=True)
barye = U(gram / gal, 'Ba', si=True)
poise = U(gram / (cm * second), 'P', si=True)
stokes = U(cm**2 / second, 'St', si=True)
kayser = U(1 / cm, si=True)
eotvos = U(1e-9 * gal / cm, 'E', si=True)
