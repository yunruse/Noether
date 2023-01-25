'''
Conventional SI-compatible units.
'''

from ..core import Unit
from ..core.prefixes import SI, SI_large, SI_small
from ..core.DisplaySet import display as I

from noether.core.config import Config, conf

from math import pi
from .si import radian, steradian, watt
from ..core.fundamental import meter, second, ampere, kilogram

percent = Unit(1/100, 'percent', '%')
permille = Unit(1/1000, 'permille', '‰')
ppm = parts_per_million = Unit(1/1_000_000, 'parts_per_million', 'ppm')

# % Spacetime

minute = Unit(second*60, 'minute', ['min'])
hour = Unit(minute * 60, 'hour', ['hr', 'h'])
day = Unit(hour * 24, "day", "d")
week = Unit(day * 7, "week", "w")
fortnight = week * 2
year = Unit(day * 365.25, "year", ["yr", "ya"], SI_large)

human_time = year & day & hour & minute & second

Config.register('human_time', True, '''\
Display time by default in human_time (years, weeks, days, etc).''')
if conf.get('human_time'):
    I(human_time)


cm = Unit(meter * 0.01, ['centimeter', 'centimetre'], 'cm')
kmph = Unit(meter*100 / hour, None, "kmph")

are = Unit(100 * meter**2, "are", "a")
hectare = Unit(100 * are, "hectare", "ha")
litre = liter = Unit((meter/10) ** 3, ["liter", "litre"], "l", SI)

ton = tonne = Unit(kilogram*1000, ["ton", "tonne"], "t", SI_large)

bpm = Unit(1 / minute, "beats per minute", "bpm")

# % Angles

deg = degree = Unit(radian * pi / 180, "degree", ["°", "deg"])
arcminute = arcmin = Unit(degree / 60, "arcminute", ["′", "arcmin"])
arcsecond = arcsec = Unit(
    degree / 3600, "arcsecond", ["″", "arcsec"], SI_small)
gradian = Unit(radian * pi / 200, "gon")

circle = turn = Unit(radian * 2*pi, "turn", "turn")
sphere = spat = Unit(steradian * 4*pi, "spat", "sp")

# % Electricity
watt_hour = Wh = Unit(watt * hour, 'watt_hour', 'Wh', SI)
amp_hour = ampere_hour = Ah = Unit(
    ampere * hour, 'amp_hour', 'Ah')
