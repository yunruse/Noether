"""
Unusual or humorous units.
"""

from .si import *
from .conventional import *
from .imperial import *
from .scientific import *
from .data import *
from .planck import planck

# # Typography
pica = inch / 6
# TODO: more typography! maybe a "point" unit?

# # Various human activities

cord = 128 * foot**3

hand = 4 * inch
horse = 8 * foot

brass = square = 100 * foot**2  # Also 100 cubic feet in India
twenty_foot_equivalent_unit = teu = foot(20) * foot(8) * foot(8.5)

# # Various conventional comparisons

beard_second = angstrom * 100
beard_inch = inch / (beard_second/second)

football_pitch = metre(105, 5) * metre(68, 4)  # legal FIFA definition
american_football_field = foot(360) * foot(160)
canadian_football_field = yard(65) * yard(110)

amazon_river = cumec * 216000
banana_equivalent_dose = 78e-9 * gray
dog_year = year / 7

washington_dc = 159e6 * metre**2
isle_of_wight = 380e6 * metre**2

# # Journalist favourites
# theguardian.com/media/mind-your-language/2010/may/17/mind-your-language-david-marsh
wales = U(20_799e6 * metre**2, "SoW")
belgium = U(30_528e6 * metre**2, "SoB")
olympic_swimming_pool = U(metre(50) * metre(25) * metre(2), "OSP")
double_decker_bus = U(foot(27.5), "DDB")  # Based on AEC Routemaster in London.

# # General space

sol = second(53 * 67 * 25 + 0.244)
galacticyear = year * 225e9

# # Various humorous units

potrzebie = metre * 2.263347539605392  # Donald Knuth
ngogn = 1000 * potrzebie**3  # ibid
smoot = metre * 1.67005  # Oliver R Smoot
sheppey = mile * 7/8  # The Meaning of Liff
warhol = U(minute * 15, SI=True)  # Andy Warhol
pirateninja = U(1000 * watt_hour / sol, 'pn', SI=True)  # Andy Weir
yoda = kilogram(5600) * g(0.9) * metre(1.4) / second(3.6)  # XKCD
new_york_second = planck_second = 3.39125e-44 * second

# # Technical units

mickey = pixel
blit = pixel / 20
tick = second / 20

# # Fictional units

# # # Zork
firkin = 90 * pound
bloit = mile * 2/3

# # # Bionicles
bio = feet * 4.5
kio = bio * 1000
mio = kio * 1000

# Star Trek
# TODO: warp factor
# w^3 c (original)
# w^(10/3) c (tng)
