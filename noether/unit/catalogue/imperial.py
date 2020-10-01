"""
Traditional imperial units.
"""

from math import pi
from .fundamental import U, candela
from .conventional import (
    cm, metre, litre,
    gram, kilogram,
    second, minute, hour
)
from .scientific import g

# # Length

inch = U(cm * 127 / 50, "in")

foot = feet = U(inch * 12, "ft")
yard = U(3 * foot, "yd")
chain = U(22 * yard, "ch")
furlong = U(10 * chain, "fur")
mile = U(8 * furlong, "mi")
league = U(3 * mile, "lea")

link = 7.92 * inch
rod = 25 * link

nauticalmile = U(1852 * metre, "nm", "NM", "nmi")

mph = mile / hour
knot = U(nauticalmile / hour, "kt", "kn")

# # Area

perch = rod**2
rood = furlong * rod
acre = furlong * chain

# # Volume

fluid_ounce = U(28.413_062_5 * litre / 1000, "fl oz")

gill = U(fluid_ounce * 5, "gi")
pint = U(gill * 4, "pt")
quart = U(2 * pint, "qt")
gallon = U(4 * quart, "gal")
peck = 2 * gallon
bushel = 4 * peck

# Mass

pound = U(453.59237 * gram, "lb")

ounce = U(pound / 16, "oz")
drachm = U(pound / 256, "dr")
grain = U(pound / 7000, "gr")

stone = U(14 * pound, "st")
quarter = U(2 * stone, "qr", "qtr")
hundredweight = U(4 * quarter, "cwt")
ton = U(2240 * pound, "t")

slug = 14.593_902_94 * kilogram

# Miscellaneous

poundforce = U(g * pound, "lbf")
poundfoot = poundforce * foot

poundal = pound * foot / second**2
psi = poundforce / inch**2

horsepower = U(33_000 * foot * poundforce / minute, "hp")
footlambert = U(candela / foot**2 / pi, 'fl')
