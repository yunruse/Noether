'''
Unusual and humorous units.
Only imported when CATALOGUE_easteregg is enabled ;)

Sources:
https://en.wikipedia.org/wiki/List_of_humorous_units_of_measurement
'''

from ...core import Unit, DisplaySet
from ...core.Prefix import SI
from ..conventional import second, meter, minute, turn, gram
from ..imperial import inch
from ..scientific import angstrom

# % Length
beard_second = Unit(
    angstrom * 100, "beard_second",
    info="According to popular convention, although the average figure is close to half of this.")


# % Time
warhol = Unit(minute * 15, "warhol", prefixes=SI,
              info="Fifteen minutes of fame")
beard_inch = Unit(inch / (beard_second/second), "beard_inch")
