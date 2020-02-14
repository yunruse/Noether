'''Math functions that support Units.'''

import math

from .catalogue import angle, dimensionless
from .function import UnaryFunction

class TrigFunc(UnaryFunction):
    input_dimension = angle
    output_dimension = dimensionless

class InvTrigFunc(UnaryFunction):
    input_dimension = dimensionless
    output_dimension = angle

# TODO: utilise Astley such that `1 / sin` simply works

class sin(TrigFunc):
    integral = lambda x: -math.cos(x)
    function = math.sin
    differential = math.cos

class cos(TrigFunc):
    integral = math.sin
    function = math.cos
    differential = lambda x: -math.sin(x)

class tan(TrigFunc):
    function = math.tan
    differential = lambda x: math.cos(x)**-2
    integral = lambda x: -math.log(math.cos(x))

class asin(InvTrigFunc):
    function = math.asin

class acos(InvTrigFunc):
    function = math.acos

class atan(InvTrigFunc):
    function = math.atan
