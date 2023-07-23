'''
CGS (centimeter-gram-second) unit system.
'''

from noether.core import Unit, UnitSet

from math import pi

from ..prefixes import SI_all, centi
from .si import SI_all, meter, kilogram, second as s
from .si import ampere, lux, coulomb, henry, ohm, volt, tesla
from .essential import turn, nit


# CGS units
gram = g = Unit(kilogram / 1000, 'gram', 'g', SI_all)
cm = centi * meter

CGS = UnitSet({cm, g, s})


# Dynamics
gal = CGS(Unit(cm/s**2, "gal", "Gal"))
dyne = CGS(Unit(gal * g, "dyne", "dyn"))
erg = CGS(Unit(dyne * cm, "erg"))
barye = CGS(Unit(g / (cm * s**2), "barye", "Ba"))
poise = CGS(Unit(g / (cm*s), "poise", "P"))
stokes = CGS(Unit(cm**2/s, "stokes", "St"))
kayser = CGS(Unit(1/cm, "kayser", "K"))

# Luminance
phot = CGS(Unit(lux / 10_000, 'phot', 'ph'))
stilb = CGS(Unit(nit * 1e4, 'stilb', 'sb'))

# EMU
abampere = abA = biot = Unit(
    ampere * 10, ["abampere", "biot"], ["abA", "Bi"])
abcoulomb = abC = Unit(coulomb * 10, "abcoulomb", "abC")
abhenry = abH = Unit(henry * 1e-9, "abhenry", "abH")
abohm = abΩ = Unit(ohm * 1e-9, "abohm", "abΩ")
abmho = absiemens = abS = Unit(1 / abohm, "absiemens", "abS")
abvolt = abV = Unit(volt * 1e-8, "abvolt", "abV")

gauss = Gs = Unit(tesla * 1e-4, "gauss", "Gs")
maxwell = Mx = Unit(gauss * cm**2, "maxwell", "Mx")
oersted = Oe = Unit(dyne / maxwell / (4*pi), "oersted", "Oe")
gilbert = Gb = Unit(abampere * turn / (4*pi), "gilbert", "Gb")


# TODO: Gaussian units https://en.wikipedia.org/wiki/Gaussian_units
# may need a config flag; dimensions are not the same as SI


# % display sets
CGS_EMU = UnitSet({CGS, abA, abC, abH, abΩ, abS, abV, Gs, Mx, Oe, Gb})
CGS = CGS_EMU
