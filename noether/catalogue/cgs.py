'''
CGS (centimeter-gram-second) unit system.
'''

from ..core import Unit, DisplaySet

from math import pi
from .conventional import second as s, gram as g, cm, turn
from .si import ampere, lux, coulomb, henry, ohm, volt, tesla

from .scientific import nit

_CGS = []


def C(unit: Unit):
    _CGS.append(unit)
    return unit


# Dynamics
gal = C(Unit(cm/s**2, "gal", "Gal"))
dyne = C(Unit(gal * g, "dyne", "dyn"))
erg = C(Unit(dyne * cm, "erg"))
barye = C(Unit(g / (cm * s**2), "barye", "Ba"))
poise = C(Unit(g / (cm*s), "poise", "P"))
stokes = C(Unit(cm**2/s, "stokes", "St"))
kayser = C(Unit(1/cm, "kayser", "K"))

# Luminance
phot = C(Unit(lux / 10_000, 'phot', 'ph'))
stilb = C(Unit(nit * 1e4, 'stilb', 'sb'))

# EMU
abampere = abA = biot = Unit(
    ampere * 10, ["abampere", "biot"], ["abA", "Bi"])
abcoulomb = abC = Unit(coulomb * 10, "abcoulomb", "abC")
abhenry = abH = Unit(henry * 1e-9, "abhenry", "abH")
abohm = abH = Unit(ohm * 1e-9, "abohm", "abΩ")
abmho = absiemens = abS = Unit(1 / abohm, "absiemens", "abS")
abvolt = abV = Unit(volt * 1e-8, "abvolt", "abV")

gauss = Gs = Unit(tesla * 1e-4, "gauss", "Gs")
maxwell = Unit(gauss * cm**2, "maxwell", "Mx")
oersted = Unit(dyne / maxwell / (4*pi), "oersted", "Oe")
gilbert = Unit(abampere * turn / (4*pi), "gilbert", "Gb")


# TODO: Gaussian units https://en.wikipedia.org/wiki/Gaussian_units
# may need a config flag; dimensions are not the same as SI


# % display sets
CGS_EMU = DisplaySet(*_CGS, abA)
CGS = CGS_EMU
