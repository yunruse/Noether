"""noether: si, si-derived and si-compatible units"""

from .unit import BaseUnit, Unit, Dimension
from math import pi

U = BaseUnit
BU = lambda dim, sym: U(1, sym, isDisplay=True, _dim=dim)

# fundamental measures, units
current = Dimension(1)
temperature = Dimension(2)
length = distance = Dimension(3)
time = Dimension(4)
mass = Dimension(5)
luminosity = Dimension(6)
substance = Dimension(7)
angle = Dimension(8)
data = Dimension(9)

amp = ampere = BU(current, "A")
kelvin = BU(temperature, "k")
meter = metre = BU(distance, "m")
second = BU(time, "s")
kilogram = BU(mass, "kg")
candela = BU(luminosity, "cd")
mole = BU(substance, "mol")
byte = BU(data, "b")

# SI derived units
frequency = time ** -1
hertz = BU(frequency, "Hz")

radian = BU(angle, "rad")
steradian = BU(angle ** 2, "sterad")

area = distance ** 2
volume = distance ** 3

# linear dynamics

velocity = speed = distance / time
acceleration = speed / time
jerk = acceleration / time

momentum = mass * speed
angular_momentum = length * momentum

force = mass * acceleration
newton = BU(force, "N")

# rotational dynamics
angular_velocity = angle / time
angular_acceleration = angular_velocity / time
angular_jerk = angular_acceleration / time

inertia = mass * angular_velocity
torque = inertia * angular_acceleration

# energy

pressure = force / area
pascal = BU(pressure, "Pa")

energy = force * distance
joule = BU(energy, "J")

power = energy / time
watt = BU(power, "W")

charge = current * time
coulomb = BU(charge, "C")

# electromagnetic

voltage = power / current
volt = BU(voltage, "V")

capacitance = charge / voltage
farad = BU(capacitance, "F")

resistance = voltage / current
ohm = BU(resistance, "Ω")
resistivity = resistance / length

conductance = resistance ** -1
siemens = BU(conductance, "S")

magneticflux = energy / current
weber = BU(magneticflux, "Wb")

magneticfluxdensity = magneticflux / area
tesla = BU(magneticfluxdensity, "T")

inductance = resistance * time
henry = BU(inductance, "H")

# radiation

lumen = BU(luminosity * angle ** 2, "lum")

illuminance = luminosity / area
lux = BU(illuminance, "Lx")

becquerel = U(hertz, "Bq")
dose = energy / mass
gray = BU(dose, "Gy")
sievert = BU(dose, "Sv")

catalyticactivity = substance / time
katal = BU(catalyticactivity, "kat")

# material

surfacetension = force / distance
density = mass / volume

thermaldiffusivity = distance**2 / time
thermalconductance = power / temperature
thermalresistance = temperature / power
thermalinsulance = temperature * area / power
thermaladmittance = power / temperature / area

# conventional si-accepted units

gram = U(kilogram / 1000, "g")
centimetre = U(metre * 0.01, "cm")
kilometre = U(metre * 1000, "km")

minute = U(second * 60, "min")
hour = U(minute * 60, "h")
day = U(hour * 24, "d")

degree = U(radian * pi / 180, "°")
angular_minute = U(degree / 60, "′")
angular_second = U(degree / 3600, "″")

acre = U(100 * metre ** 2, "a")
hectare = U(100 * acre, "ha")
litre = U((metre / 10) ** 3, "l")
tonne = U(kilogram * 1000, "t")

# scientific units

parsec = U(3.0857e16 * metre, "pc")
au = U(1.495_878_707e11 * metre, "au")
solar_mass = U(1.98802e30 * kilogram, "msol")

dalton = U(1.660_538_86e-27 * kilogram, "u")

# commonly-used metric variants

angstrom = U(metre * 1e-10, "å")
are = U((10 * metre) ** 2, "a")
barn = U(1e-28 * metre ** 2, "b")

bar = U(1e5 * pascal, "bar")
millibar = U(100 * pascal, "mbar")
atmosphere = U(101_325 * pascal, "atm")
torr = U(atmosphere / 760, "torr")
millimetre_mercury = mmhg = U(133.322_387_415 * pascal, "mmhg")

calorie = U(4.814 * joule, "cal")
kilocalorie = U(calorie * 1000, "kcal")

# older cgs units

gal = centimetre / second ** 2
dyne = gram * gal
erg = dyne * centimetre
barye = gram / (centimetre * second ** 2)
poise = gram / (centimetre * second)
stokes = centimetre ** 2 / second
kayser = 1 / centimetre

# imperial length and area

inch = U(centimetre * 127 / 50, "in")
foot = U(inch * 12, "ft")
yard = U(3 * foot, "yd")
chain = U(22 * yard, "ch")
furlong = U(10 * chain, "fur")
mile = U(8 * furlong, "mi")
league = U(3 * mile, "lea")

link = 7.92 * inch
rod = 25 * link

perch = rod ** 2
rood = furlong * rod
acre = furlong * chain

# imperial volume

fluid_ounce = U(28.413_062_5 * litre / 1000, "fl oz")

gill = U(fluid_ounce * 5, "gi")
pint = U(gill * 4, "pt")
quart = U(2 * pint, "qt")
gallon = U(4 * quart, "gal")
peck = 2 * gallon
bushel = 4 * peck

# imperial weight

pound = U(453.59237 * gram, "lb")

ounce = U(pound / 16, "oz")
drachm = U(pound / 256, "dr")
grain = U(pound / 7000, "gr")

stone = U(14 * pound, "st")
quarter = U(2 * stone, "qr", "qtr")
hundredweight = U(4 * quarter, "cwt")
ton = U(2240 * pound, "t")

slug = 14.593_902_94 * kilogram

# speeds

mps = metre / second
mph = mile / hour
kmph = kilometre / hour

nauticalmile = U(1852 * metre, "nm", "NM", "nmi")
knot = U(nauticalmile / hour, "kt", "kn")

# conventional time units
week = day * 7
fortnight = week * 2
year = U(day * 365.25, "yr")

# unusual units

hand = 4 * inch
horse = 8 * foot
footballpitch = 105 * 68 * metre ** 2

wales = 20799 * kilometre ** 2

dogyear = year / 7
sol = 88775 * second
galacticyear = 225 * 1e9 * year

firkin = 90 * pound
smoot = 1.67005 * metre

# name transmogrification

__all__ = []

units = dict(globals()).items()

for name, unit in units:
    displayName = name.replace('_', ' ')
    if isinstance(unit, Dimension):
        Dimension._names[unit] = displayName
    elif isinstance(unit, BaseUnit):
        unit.symbols += (displayName,)
    elif isinstance(unit, Unit):
        globals()[name] = U(unit, name)
    else:
        continue

    __all__.append(name)

if __name__ == "__main__":
    # display a table of symbols

    table = []
    for name in __all__:
        unit = globals()[name]

        measure = str(unit.measure).replace("none", "unknown").replace("unitless", "")
        table.append([name, unit.numberstring(), unit.symbol, measure])

    from .helpers import tablify

    print("\n".join(tablify(sorted(table, key=lambda q: q[3]))))