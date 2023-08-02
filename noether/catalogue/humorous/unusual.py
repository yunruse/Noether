'''
Unusual units of measure which no doubt are still of some use.

Sources:
https://en.wikipedia.org/wiki/List_of_humorous_units_of_measurement
'''

from noether.core import Unit, UnitSet

from ..prefixes import SI_all
from ..fundamental import second
from ..scientific import minute, watt_hour, sievert, angstrom, sol
from ..conventional import inch, hour, year

# % Length
beard_second = Unit(
    angstrom * 100, "beard_second",
    info="According to popular convention, although the average figure is close to half of this.")

# % Time
warhol = Unit(minute * 15, "warhol", prefixes=SI_all,
              info="Warhol's \"fifteen minutes of fame\"")
beard_inch = Unit(inch / (beard_second/second), "beard_inch")

dog_year = Unit(
    year / 7, "dog_year",
    info="This is a very approximate measure and dependent on breed and size")

# % Energy and radiation
# https://blog.xkcd.com/2011/03/19/radiation-chart/
BED = banana_equivalent_dose = Unit(
    sievert * 1e-7, "banana_equivalent_dose", "BED",
    info="c.f. xkcd radiation chart for other useful radiation units")
flight_dose_rate = Unit(
    sievert * 4e-9 / hour, "flight_dose_rate", "FED",
    info="Standardised ionizing radiation at 10km cruising altitude")

pirate_ninja = Unit(
    watt_hour * 1000 / sol, "pirate_ninja", "pn",
    info="1 kWh per Martian day, from Andy Weir's The Martian")
