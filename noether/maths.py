'''Math functions that support Units.'''

import math

from .unitCatalogue import angle, dimensionless
from .function import UnaryFunction

class _trig_in(UnaryFunction):
    input_dimension = angle
    output_dimension = dimensionless

class _trig_out(UnaryFunction):
    input_dimension = dimensionless
    output_dimension = angle

# TODO: figure out algebra via Astley to have these support true calculus
# such that 'differential = -cos' and 'sec = 1 / cos' are possible

class sin(_trig_in):
    integral = lambda x: -math.cos(x)
    function = math.sin
    differential = math.cos

class cos(_trig_in):
    integral = math.sin
    function = math.cos
    differential = lambda x: -math.sin(x)

class tan(_trig_in):
    function = math.tan
    differential = lambda x: math.cos(x)**-2
    integral = lambda x: -math.log(math.cos(x))

class asin(_trig_out):
    function = math.asin

class acos(_trig_out):
    function = math.acos

class atan(_trig_out):
    function = math.atan