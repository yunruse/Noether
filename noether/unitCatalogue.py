"""
noether: Catalogue of as many units and dimensions as are known.

Contains SI, SI-derived, SI-compatible, IEC, imperial, and many obscure units.

Be warned that the egregious use of globals WILL frustrate your linter.
"""

from .measure import Unit, Measure, Dimension
from .scale import prefix_SI, prefix_IEC
from math import pi, log

prefixable_SI = set()
prefixable_IEC = set()


def U(value, *symbols, display=None, SI=False, IEC=False):
    display = SI if display is None else display
    unit = Unit(value, *symbols, isDisplay=display)
    if SI:
        prefixable_SI.add(unit)
    if IEC:
        prefixable_IEC.add(unit)
    return unit


# SI units

def base_units():
    # yapf: disable
    _BASE_UNITS = (
        (1, "luminosity", "cd", True, "candela"),
        (2, "current", "A", True, "amp", "ampere"),
        (3, "temperature", "K", True, "kelvin"),
        (4, "mass", "kg", False, "kilogram"),
        (5, "substance", "mol", True, "mole"),
        (6, "length", "m", True, "metre", "meter"),
        (7, "time", "s", True, "second")
    )
    # yapf: enable

    for u in _BASE_UNITS:
        display_order, name, symbol, SI, *units = u
        dim = Dimension.new(display_order, name, symbol)
        globals()[name] = dim
        unit = U(dim, symbol, SI=SI)
        for name in units:
            globals()[name] = unit

base_units()
del base_units

dimensionless = Dimension()

distance = length

# SI derived units
frequency = time**-1
hertz = U(frequency, "Hz", SI=True)
bpm = U(hertz / 60, "bmp")

area = length**2
volume = length**3

angle = Dimension.new(3.2, "angle", "rad")
radian = U(angle, "rad", SI=True)
steradian = U(angle**2, "sterad", SI=True)

# derivatives and integrals of time

velocity = speed = distance / time
acceleration = speed / time
jerk = acceleration / time
jounce = snap = jerk / time
crackle = snap / time
pop = crackle / time
lock = pop / time
drop = pop / time

absement = distance * time
absity = absement * time
abseleration = absity * time
abserk = abseleration * time
absounce = abserk * time

# dynamics

momentum = mass * speed
angular_momentum = length * momentum

force = weight = mass * acceleration
newton = U(force, "N", SI=True)

angular_velocity = angle / time
angular_acceleration = angular_velocity / time
angular_jerk = angular_acceleration / time

inertia = mass * angular_velocity
torque = inertia * angular_acceleration

# energy

pressure = force / area
pascal = U(pressure, "Pa", SI=True)

energy = torque = force * distance
joule = U(energy, "J", SI=True)

power = energy / time
watt = U(power, "W", SI=True)

# electricity

charge = current * time
coulomb = U(charge, "C", SI=True)

voltage = power / current
volt = U(voltage, "V", SI=True)

capacitance = charge / voltage
farad = U(capacitance, "F", SI=True)

resistance = voltage / current
ohm = U(resistance, "Ω", SI=True)
resistivity = resistance / length

conductance = resistance**-1
siemens = U(conductance, "S", SI=True)

inductance = resistance * time
henry = U(inductance, "H", SI=True)
reluctance = 1 / inductance

capicitive_reactance = capacitance * angular_velocity
inductive_reactance = inductance * angular_velocity

permeability = inductance * length / area
permittivity = capacitance * length / area

# magnetism

magnetic_flux = energy / current
weber = U(magnetic_flux, "Wb", SI=True)

magnetic_flux_density = magnetic_flux / area
tesla = U(magnetic_flux_density, "T", SI=True)

magnetic_moment = current * area

magnetisation = magnetic_moment / volume

# radiation

lumen = U(luminosity * angle**2, "lum", SI=True)

illuminance = luminosity / area
lux = U(illuminance, "Lx", SI=True)

irradiance = power / area
intensity = power / area
heat_flux = power / area

becquerel = U(hertz, "Bq")
dose = energy / mass
gray = U(dose, "Gy")
sievert = U(dose, "Sv")

# chemistry

catalytic_activity = substance / time
katal = U(catalytic_activity, "kat")

reaction_rate = substance / (volume * time)

# material

linear_density = mass / length
area_density = mass / area
density = mass / volume
specific_volume = volume / mass

specific_energy = energy / mass
molar_energy = energy / substance

heat_capacity = entropy = energy / temperature
specific_heat_capacity = heat_capacity / mass
molar_heat_capacity = heat_capacity / substance

surface_tension = force / length
viscosity = pressure * time

# thermal

thermal_conductance = power / temperature
thermal_conductivity = thermal_conductance * length / area
thermal_resistance = temperature / power
thermal_resistivity = thermal_resistance * length / area

met = 58.2 * watt / metre ** 2

# conventional si-accepted units

gram = U(kilogram / 1000, "g", SI=True)

minute = U(second * 60, "min")
hour = U(minute * 60, "h")
day = U(hour * 24, "d")

degree = U(radian * pi / 180, "°")
angular_minute = U(degree / 60, "′")
angular_second = U(degree / 3600, "″")

acre = U(100 * metre**2, "a")
hectare = U(100 * acre, "ha")
litre = U((metre / 10)**3, "l", SI=True)
tonne = ton = U(kilogram * 1000, "t", SI=True)

# scientific units

parsec = U(3.0857e16 * metre, "pc")
au = U(1.495_878_707e11 * metre, "au")
solar_mass = U(1.98802e30 * kilogram, "msol")

dalton = U(1.660_538_86e-27 * kilogram, "u")

# commonly-used metric variants

angstrom = U(metre * 1e-10, "å")
are = U((10 * metre)**2, "a")
barn = U(1e-28 * metre**2, "b")

g = 9.980665 * metre / second**2
gee = g * kilogram

bar = U(1e5 * pascal, "bar", SI=True, display=False)
atmosphere = U(101_325 * pascal, "atm", display=False)
torr = U(atmosphere / 760, "torr")
metre_mercury = meter_mercury = U(133_322.387_415 * pascal, "mhg", SI=True)

calorie = U(4.814 * joule, "cal", SI=True, display=False)
kilocalorie = kcal = U(calorie * 1000, "kcal")

# older cgs units

cm = meter / 100

gal = cm / second**2
dyne = gram * gal
erg = dyne * cm
barye = gram / gal
poise = gram / (cm * second)
stokes = cm**2 / second
kayser = 1 / cm
inch = U(cm * 127 / 50, "in")

del cm

# imperial length and area

foot = U(inch * 12, "ft")
yard = U(3 * foot, "yd")
chain = U(22 * yard, "ch")
furlong = U(10 * chain, "fur")
mile = U(8 * furlong, "mi")
league = U(3 * mile, "lea")

link = 7.92 * inch
rod = 25 * link

perch = rod**2
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

# imperial insanity

poundforce = U(gee * pound, "lbf")
poundfoot = poundforce * foot

poundal = pound * foot / second**2
psi = pound / inch**2

# speeds

mps = metre / second
mph = mile / hour
kmph = meter * 1000 / hour

nauticalmile = U(1852 * metre, "nm", "NM", "nmi")
knot = U(nauticalmile / hour, "kt", "kn")

# conventional time units
week = day * 7
fortnight = week * 2
year = U(day * 365.25, "yr")

# unusual units

hand = 4 * inch
horse = 8 * foot
footballpitch = 105 * 68 * metre**2

wales = 20799e6 * meter**2

dogyear = year / 7
sol = 88775 * second
galacticyear = 225 * 1e9 * year

firkin = 90 * pound
smoot = 1.67005 * metre

# data & IEC prefixes

data = Dimension.new(3.5, "data", "B")

byte = U(data, "B", SI=True, IEC=True)
bit = shannon = U(byte / 8, "b", SI=True, IEC=True)
nat = U(bit / log(2), 'nat', SI=True)
trit = nat * log(3)
hartley = ban = dit = U(nat * log(10), 'Hart')

data_rate = data / time
bps = U(bit / second, 'bps', SI=True, IEC=True)

Measure.display(bps)

# image size
pixel_count = Dimension.new(3.4, "pixel_count", "P")
pixel = U(pixel_count, SI=True)

pixel_fill_rate = pixel_count / time
image_density = pixel_count / data
image_quality = pixel_count / length

ppi = U(pixel / inch, 'ppi')
Measure.display(ppi)

# name transmogrification

__all__ = []

units = dict(globals()).items()

for name, unit in units:
    displayName = name.replace("_", " ")
    if isinstance(unit, Dimension):
        unit.addName(name)
    elif isinstance(unit, Unit):
        unit.names += (displayName, )
    elif isinstance(unit, Measure):
        globals()[name] = unit = U(unit, name)
    else:
        continue

    __all__.append(name)

for units, prefixes in (
    (prefixable_SI, prefix_SI),
    (prefixable_IEC, prefix_IEC)
):
    for unit in units:
        for pName, pSym, pFactor in prefixes:
            for names, prefix in ((unit.names, pName), (unit.symbols, pSym)):
                for name in names:
                    name = prefix + name.replace(" ", "_")
                    if name not in globals():
                        globals()[name] = unit * pFactor
                        __all__.append(name)
