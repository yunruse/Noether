'''
Conventional SI-compatible units.
'''

from noether.core import Unit, AffineUnit
from noether.core import display
from noether.config import Config, conf

from math import pi

from ..prefixes import SI_all, SI_large, SI_small
from ..scientific import meter, second, kilogram, kelvin
from ..scientific import radian, turn
from ..scientific import turn
from ..scientific import day, hour, minute
from ..scientific import gram

# % Ratio
percent = Unit(1/100, 'percent', '%')
permille = Unit(1/1000, 'permille', '‰')
ppm = parts_per_million = Unit(1/1_000_000, 'parts_per_million', 'ppm')
proof = Unit(0.5, 'proof', '°', info='alcohol purity')
karat = Unit(
    1 / 24, 'karat', 'Kt',
    info="Used in gold purity; 24Kt is pure or near-pure."
    " Increasingly deprecated for millesimal fineness."
    " Not to be confused with the carat.")

# % Temperature
celsius = degC = AffineUnit(kelvin*1, kelvin*273.15, "celsius", "°C")

# % Time
week = Unit(day * 7, "week", "w")
fortnight = week * 2
year_gregorian = Unit(
    day * 365.2425, 'year', ["yr", "ya"], SI_large,
    info="Gregorian definition")
year = year_gregorian

# % Distance
km = kilometer = kilometre = Unit(
    meter * 1000, ['kilometer', 'kilometre'], 'km')
kmph = Unit(km / hour, None, "kmph")

marathon = Unit(
    km * 42.195, "marathon",
    info="Race length based on Greek legend, set by convention from 1908 Summer Olympics"
)

# % Area
are = Unit(100 * meter**2, "are", "a")
hectare = Unit(100 * are, "hectare", "ha")

# % Volume
litre = liter = L = Unit((meter/10) ** 3, ["liter", "litre"], "l", SI_all)
milliliter = milliliter = ml = mL = Unit(
    liter / 1000, ['milliliter', 'millilitre'], 'mL')

# % Mass & density
ton = tonne = Unit(
    kilogram*1000, ["ton", "tonne"], "t", SI_large, info="metric")
gsm = Unit(
    gram / meter**2, "gram per square meter", "gsm",
    info="Used especially in paper-making as a proxy for thickness and pliability. "
    " A standard sheet of printer paper is usually 100gsm.")
carat = Unit(
    gram * 0.2, "carat", "ct",
    info="Used to measure the mass of gemstones and pearls."
    " Not to be confused with the karat.")

# % Frequency & angle
bpm = Unit(1 / minute, "beats per minute", "bpm")

deg = degree = Unit(radian * pi / 180, "degree", ["°", "deg"])
arcminute = arcmin = Unit(degree / 60, "arcminute", ["′", "arcmin"])
arcsecond = arcsec = Unit(
    degree / 3600, "arcsecond", ["″", "arcsec"], SI_small)


# % Display
Config.register('UNITS_conventional_time', True, '''\
Display time in year & day & hour & minute & second.''')
if conf.get('UNITS_conventional_time'):
    display(year & day & hour & minute & second)


Config.register('UNITS_conventional_angles', True, '''\
Display angles in turn & degree & arcminute & arcsecond.''')
if conf.get('UNITS_conventional_angles'):
    display(turn & degree & arcminute & arcsecond)
