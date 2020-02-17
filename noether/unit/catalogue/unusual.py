"""
Unusual or humorous units.
"""

from .si import *
from .conventional import *
from .imperial import *
from .scientific import *
from .data import *
from .planck import planck

hand = 4 * inch
horse = 8 * foot

beard_second = angstrom * 100
beard_inch = inch / (beard_second/second)

# conventional comparisons
football_pitch = 105 * 68 * metre**2
wales = 20799e6 * metre**2
amazon_river = cumec * 216000
banana_equivalent_dose = 78e-9 * gray

# photometric units, some deprecated
fresnel = (1 / second)(1e12)

nit = U(candela / metre**2, 'nt')
stilb = U(candela / cm**2, 'sb')
apostilb = blondel = U(nit / pi, 'asb')
lambert = U(stilb / pi, 'L')
skot = U(apostilb / 1000, 'sk')
bril = U(skot / 10_000, 'bril')
footlambert = U(candela / foot**2 / pi, 'fl')

# general space
sol = second(53 * 67 * 25 + 0.244)
galacticyear = year * 225e9

# Various humorous units
potrzebie = metre * 2.263347539605392  # Donald Knuth
ngogn = 1000 * potrzebie**3  # ibid
smoot = metre * 1.67005  # Oliver R Smoot
sheppey = mile * 7/8  # The Meaning of Liff
warhol = U(minute * 15, SI=True)  # Andy Warhol
pirateninja = U(1000 * watt_hour / sol, 'pn', SI=True)  # Andy Weir
yoda = kilogram(5600) * g(0.9) * metre(1.4) / second(3.6)  # XKCD

new_york_second = planck.time
dogyear = year / 7
mickey = pixel
blit = pixel / 20
tick = second / 20

# Zork
firkin = 90 * pound
bloit = mile * 2/3

# Bionicles
bio = feet * 4.5
kio = bio * 1000
mio = kio * 1000

# Star Trek
# TODO: warp factor
# w^3 c (original)
# w^(10/3) c (tng)
