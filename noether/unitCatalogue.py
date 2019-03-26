"""Noether: SI, SI-derived and SI-compatible units"""

from .unit import BaseUnit, Unit, Dimension
from math import pi

U = BaseUnit
BU = lambda dim, sym: U(1, sym, isDisplay=True, _dim=dim)

# Fundamental measures, units
Current = Dimension(1)
Temperature = Dimension(2)
Distance = Dimension(3)
Time = Dimension(4)
Mass = Dimension(5)
Luminosity = Dimension(6)
Substance = Dimension(7)
Angle = Dimension(8)

Length = Distance

Ampere = BU(Current, "A")
Kelvin = BU(Temperature, "k")
Meter = Metre = BU(Distance, "m")
Second = BU(Time, "s")
Kilogram = BU(Mass, "kg")
Candela = BU(Luminosity, "cd")
Mole = BU(Substance, "mol")

# SI Derived units

Frequency = Time ** -1
Hertz = BU(Frequency, "Hz")

Radian = BU(Angle, "rad")
Steradian = BU(Angle ** 2, "sterad")

Area = Distance ** 2
Volume = Distance ** 3

# Linear dynamics

Velocity = Speed = Distance / Time
Acceleration = Speed / Time
Jerk = Acceleration / Time

Momentum = Mass * Speed
AngularMomentum = Length * Momentum

Force = Mass * Acceleration
Newton = BU(Force, "N")

# Energy

Pressure = Force / Area
Pascal = BU(Pressure, "Pa")

Energy = Force * Distance
Joule = BU(Energy, "J")

Power = Energy / Time
Watt = BU(Power, "W")

Charge = Current * Time
Coulomb = BU(Charge, "C")

# Electromagnetic

Voltage = Power / Current
Volt = BU(Voltage, "V")

Capacitance = Charge / Voltage
Farad = BU(Capacitance, "F")

Resistance = Voltage / Current
Ohm = BU(Resistance, "Ω")
Resistivity = Resistance / Length

Conductance = Resistance ** -1
Siemens = BU(Conductance, "S")

MagneticFlux = Energy / Current
Weber = BU(MagneticFlux, "Wb")

MagneticFluxDensity = MagneticFlux / Area
Tesla = BU(MagneticFluxDensity, "T")

Inductance = Resistance * Time
Henry = BU(Inductance, "H")

# Radiation

Lumen = BU(Luminosity * Angle ** 2, "lum")

Illuminance = Luminosity / Area
Lux = BU(Illuminance, "lx")

Becquerel = U(Hertz, "Bq")
Dose = Energy / Mass
Gray = BU(Dose, "Gy")
Sievert = BU(Dose, "Sv")

CatalyticActivity = Substance / Time
Katal = BU(CatalyticActivity, "kat")

# Material

SurfaceTension = Force / Distance
Density = Mass / Volume

ThermalDiffusivity = Distance**2 / Time
ThermalConductance = Power / Temperature
ThermalResistance = Temperature / Power
ThermalInsulance = Temperature * Area / Power
ThermalAdmittance = Power / Temperature / Area

# Conventional SI-accepted units

Gram = U(Kilogram / 1000, "g")
Centimetre = U(Metre * 0.01, "cm")
Kilometre = U(Metre * 1000, "km")

Minute = U(Second * 60, "min")
Hour = U(Minute * 60, "h")
Day = U(Hour * 24, "d")

Degree = U(Radian * pi / 180, "°")
RadialMinute = U(Degree / 60, "′")
RadialSecond = U(Degree / 3600, "″")

Acre = U(100 * Metre ** 2, "a")
Hectare = U(100 * Acre, "ha")
Litre = U((Metre / 10) ** 3, "L")
Tonne = U(Kilogram * 1000, "t")

# Scientific units

Parsec = U(3.0857e16 * Metre, "pc")
AU = U(1.495_878_707e11 * Metre, "AU")
SolarMass = U(1.98802e30 * Kilogram, "Msol")

u = Dalton = U(1.660_538_86e-27 * Kilogram, "u")

# Commonly-used metric variants

Angstrom = U(Metre * 1e-10, "Å")
Are = U((10 * Metre) ** 2, "a")
Barn = U(1e-28 * Metre ** 2, "b")

Bar = U(1e5 * Pascal, "bar")
Millibar = U(100 * Pascal, "mbar")
Atmosphere = U(101_325 * Pascal, "atm")
Torr = U(Atmosphere / 760, "Torr")
MillimetreMercury = mmHg = U(133.322_387_415 * Pascal, "mmHg")

Calorie = U(4.814 * Joule, "cal")
Kilocalorie = U(Calorie * 1000, "kCal")

# Older CGS units

Gal = Centimetre / Second ** 2
Dyne = Gram * Gal
Erg = Dyne * Centimetre
Barye = Gram / (Centimetre * Second ** 2)
Poise = Gram / (Centimetre * Second)
Stokes = Centimetre ** 2 / Second
Kayser = 1 / Centimetre

# Imperial length and area

Inch = U(Centimetre * 127 / 50, "in")
Foot = U(Inch * 12, "ft")
Yard = U(3 * Foot, "yd")
Chain = U(22 * Yard, "ch")
Furlong = U(10 * Chain, "fur")
Mile = U(8 * Furlong, "mi")
League = U(3 * Mile, "lea")

Link = 7.92 * Inch
Rod = 25 * Link

Perch = Rod ** 2
Rood = Furlong * Rod
Acre = Furlong * Chain

# Imperial volume

FluidOunce = U(28.413_062_5 * Litre / 1000, "fl oz")

Gill = U(FluidOunce * 5, "gi")
Pint = U(Gill * 4, "pt")
Quart = U(2 * Pint, "qt")
Gallon = U(4 * Quart, "gal")
Peck = 2 * Gallon
Bushel = 4 * Peck

# Imperial weight

Pound = U(453.59237 * Gram, "lb")

Ounce = U(Pound / 16, "oz")
Drachm = U(Pound / 256, "dr")
Grain = U(Pound / 7000, "gr")

Stone = U(14 * Pound, "st")
Quarter = U(2 * Stone, "qr", "qtr")
Hundredweight = U(4 * Quarter, "cwt")
Ton = U(2240 * Pound, "t")

Slug = 14.593_902_94 * Kilogram

# Speeds

mps = Metre / Second
mph = Mile / Hour
kmph = Kilometre / Hour

NauticalMile = U(1852 * Meter, "M", "NM", "nmi")
Knot = U(NauticalMile / Hour, "kt", "kn")

# Conventional time units
Week = Day * 7
Fortnight = Week * 2
Year = U(Day * 365.25, "yr")

# Unusual units

Hand = 4 * Inch
Horse = 8 * Foot
FootballPitch = 105 * 68 * Metre ** 2

Wales = 20799 * Kilometre ** 2

DogYear = Year / 7
Sol = 88775 * Second
GalacticYear = 225 * 1e9 * Year

Firkin = 90 * Pound
Smoot = 1.67005 * Metre

# Name transmogrification

__all__ = []

units = dict(globals()).items()

for name, unit in units:
    if isinstance(unit, Dimension):
        Dimension._names[unit] = name
    elif isinstance(unit, BaseUnit):
        unit.symbols += (name,)
    elif isinstance(unit, Unit):
        globals()[name] = U(unit, name)
    else:
        continue

    __all__.append(name)

if __name__ == "__main__":
    # Display a table of symbols

    table = []
    for name in __all__:
        unit = globals()[name]

        measure = str(unit.measure).replace("None", "unknown").replace("unitless", "")
        table.append([name, unit.numberString(), unit.symbol, measure])

    from .helpers import tablify

    print("\n".join(tablify(sorted(table, key=lambda q: q[3]))))
