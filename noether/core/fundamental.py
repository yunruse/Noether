'''
Fundamental units.
'''

from .Dimension import Dimension
from .Measure import Measure
from .Unit import Unit
from .prefixes import SI
from .DisplaySet import display as I

luminosity = I(Dimension.new('luminosity', 'J', -7), 'luminosity')
current = I(Dimension.new('current', 'I', -6), 'current')
temperature = I(Dimension.new('temperature', 'Θ', -5), 'temperature')
mass = I(Dimension.new('mass', 'M', -4), 'mass')
substance = I(Dimension.new('substance', 'N', -3), 'substance')
length = I(Dimension.new('length', 'L', -2), 'length')
time = I(Dimension.new('time', 'T', -1), 'time')

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
