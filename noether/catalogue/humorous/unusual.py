'''
Unusual units of measure which no doubt are still of some use.

Sources:
https://en.wikipedia.org/wiki/List_of_humorous_units_of_measurement
'''

from noether.core import Unit, UnitSet

from ..prefixes import SI_all
from ..fundamental import second
from ..scientific import minute, watt_hour, sievert, angstrom, sol
from ..conventional import inch

U = UNUSUAL = UnitSet()

# % Length
beard_second = Unit(
    angstrom * 100, "beard_second",
    info="According to popular convention, although the average figure is close to half of this.")

# % Time
warhol = Unit(minute * 15, "warhol", prefixes=SI_all,
              info="Warhol's \"fifteen minutes of fame\"")
beard_inch = Unit(inch / (beard_second/second), "beard_inch")


# % Energy and radiation
BED = banana_equivalent_dose = Unit(
    sievert * 1e-7, "banana_equivalent_dose", "BED",
    info="c.f. xkcd radiation chart for other useful radiation units")
# https://blog.xkcd.com/2011/03/19/radiation-chart/

pirate_ninja = Unit(
    watt_hour * 1000 / sol, "pirate_ninja", "pn",
    info="from the book The Martian")
