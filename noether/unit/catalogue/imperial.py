from .fundamental import U
from .conventional import (
    cm, metre, litre,
    gram, kilogram,
    second, hour
)
from .scientific import gee

# length and area

inch = U(cm * 127 / 50, "in")

foot = U(inch * 12, "ft")
yard = U(3 * foot, "yd")
chain = U(22 * yard, "ch")
furlong = U(10 * chain, "fur")
mile = U(8 * furlong, "mi")
league = U(3 * mile, "lea")

mph = mile / hour

nauticalmile = U(1852 * metre, "nm", "NM", "nmi")
knot = U(nauticalmile / hour, "kt", "kn")

link = 7.92 * inch
rod = 25 * link

perch = rod**2
rood = furlong * rod
acre = furlong * chain

# volume

fluid_ounce = U(28.413_062_5 * litre / 1000, "fl oz")

gill = U(fluid_ounce * 5, "gi")
pint = U(gill * 4, "pt")
quart = U(2 * pint, "qt")
gallon = U(4 * quart, "gal")
peck = 2 * gallon
bushel = 4 * peck

# weight

pound = U(453.59237 * gram, "lb")

ounce = U(pound / 16, "oz")
drachm = U(pound / 256, "dr")
grain = U(pound / 7000, "gr")

stone = U(14 * pound, "st")
quarter = U(2 * stone, "qr", "qtr")
hundredweight = U(4 * quarter, "cwt")
ton = U(2240 * pound, "t")

slug = 14.593_902_94 * kilogram

# miscellanea

poundforce = U(gee * pound, "lbf")
poundfoot = poundforce * foot

poundal = pound * foot / second**2
psi = pound / inch**2