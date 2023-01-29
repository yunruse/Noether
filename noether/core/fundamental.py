'''
Fundamental units.
'''

from .Dimension import Dimension
from .Measure import Measure
from .Unit import Unit
from .Prefix import SI
from .DisplaySet import display as I

luminosity = Dimension.new('luminosity', 'J', -7)
current = Dimension.new('current', 'I', -6)
temperature = Dimension.new('temperature', 'Θ', -5)
mass = Dimension.new('mass', 'M', -4)
substance = Dimension.new('substance', 'N', -3)
length = Dimension.new('length', 'L', -2)
time = Dimension.new('time', 'T', -1)

candela = cd = I(Unit(
    Measure(dim=luminosity), 'candela', 'cd', SI))
ampere = A = I(Unit(
    Measure(dim=current), 'ampere', 'A', SI))
kelvin = K = I(Unit(
    Measure(dim=temperature), 'kelvin', 'K', SI))
kilogram = kg = I(Unit(
    Measure(dim=mass), 'kilogram', 'kg'))
mole = mol = I(Unit(
    Measure(dim=substance), 'mole', 'mol', SI))
meter = metre = m = I(Unit(
    Measure(dim=length), ['meter', 'metre'], 'm', SI))
second = s = I(Unit(
    Measure(dim=time), 'second', 's', SI))

__all__ = [
    'luminosity', 'candela', 'cd',
    'current', 'ampere', 'A',
    'temperature', 'kelvin', 'K',
    'mass', 'kilogram', 'kg',
    'substance', 'mole', 'mol',
    'length', 'meter', 'm', 'metre',
    'time', 'second', 's',
]
