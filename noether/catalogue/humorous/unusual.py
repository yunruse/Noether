'''
Unusual units of measure which no doubt are still of some use.

Sources:
https://en.wikipedia.org/wiki/List_of_humorous_units_of_measurement
'''

from ...core import Unit, DisplaySet
from ...core.Prefix import SI
from ..conventional import second, minute, watt_hour
from ..si import sievert
from ..scientific import angstrom, sol
from ..imperial import inch

U = UNUSUAL = DisplaySet()

# % Length
beard_second = Unit(
    angstrom * 100, "beard_second",
    info="According to popular convention, although the average figure is close to half of this.")

# % Time
warhol = Unit(minute * 15, "warhol", prefixes=SI,
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