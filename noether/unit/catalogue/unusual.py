"""
Unusual or humorous units.
"""

from .si import *
from .conventional import *
from .imperial import *
from .scientific import *
from .data import *

hand = 4 * inch
horse = 8 * foot

potrzebie = metre * 2.263347539605392
ngogn = 1000 * potrzebie**3
smoot = metre * 1.67005
sheppey = mile * 7/8

new_york_second = planck_second = 3.39125e-44 * second

friedman = year / 2
warhol = U(minute * 15, SI=True)

beard_second = angstrom * 100
beard_inch = inch / (beard_second/second)

football_pitch = metre(105, 5) * metre(68, 4)  # legal FIFA definition
american_football_field = foot(360) * foot(160)
canadian_football_field = yard(65) * yard(110)

wales = 20799e6 * metre**2
dogyear = year / 7
amazon_river = cumec * 216000
sverdrup = U(cumec * 1e6, "Sv")
banana_equivalent_dose = 78e-9 * gray

mickey = pixel

sol = 88775 * second
galacticyear = 225 * 1e9 * year

firkin = 90 * pound
bloit = mile * 2/3  # zork
