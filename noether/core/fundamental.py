'''
Fundamental units.
'''

from .Dimension import Dimension
from .Measure import Measure
from .Unit import Unit
from .prefixes import SI
from .DisplaySet import display as I

BASE_UNITS = [
    # display_order, name, dimension symbol,
    #   is base for prefixes, unit symbol, unit names
    (-3, "luminosity",  "J",
        True, "cd", ["candela"]),
    (-2, "current", "I",
        True, "A", ["amp", "ampere"]),
    (-1, "temperature", "Θ",
        True, "K", ["kelvin"]),
    (1, "mass", "M",
        False, "kg", ["kilogram"]),
    (2, "substance", "N",
        True, "mol", ["mole"]),
    (3, "length", "L",
        True, "m", ["metre", "meter"]),
    (4, "time", "T",
        True, "s", ["second"]),
]

luminosity = Dimension.new('luminosity', 'J', -7)
current = Dimension.new('current', 'I', -6)
temperature = Dimension.new('temperature', 'Θ', -5)
mass = Dimension.new('mass', 'M', -4)
substance = Dimension.new('substance', 'N', -3)
length = Dimension.new('length', 'L', -2)
time = Dimension.new('time', 'T', -1)

candela = I(Unit(
    Measure(dim=luminosity), 'candela', 'cd', SI))
ampere = I(Unit(
    Measure(dim=current), 'ampere', 'amp', SI))
kelvin = I(Unit(
    Measure(dim=temperature), 'kelvin', 'K', SI))
kilogram = I(Unit(
    Measure(dim=mass), 'kilogram', 'kg'))
mole = I(Unit(
    Measure(dim=substance), 'mole', 'mol', SI))
meter = metre = I(Unit(
    Measure(dim=length), ['meter', 'metre'], 'm', SI))
second = I(Unit(
    Measure(dim=time), 'second', 's', SI))

gram = Unit(kilogram / 1000, 'gram', 'g', SI)

__all__ = [
    'luminosity',
    'current',
    'temperature',
    'mass',
    'substance',
    'length',
    'time',
    'candela',
    'ampere',
    'kelvin',
    'kilogram',
    'mole',
    'meter',
    'metre',
    'second',
    'gram'
]
