from functools import wraps
import math
from math import radians as rad, degrees as deg

from .helpers import _asNamed

class TrigonometryState:
    def __init__(self, useRadians=True):
        self.radians = useRadians

    def _out(self, x):
        return x if self.radians else deg(x)

    def _in(self, x):
        return x if self.radians else rad(x)
    
    sin = wraps(math.sin)(lambda s, x: math.sin(s._in(x)))
    cos = wraps(math.cos)(lambda s, x: math.cos(s._in(x)))
    tan = wraps(math.tan)(lambda s, x: math.tan(s._in(x)))
    
    asin = wraps(math.asin)(lambda s, x: s._out(math.asin(x)))
    acos = wraps(math.asin)(lambda s, x: s._out(math.acos(x)))
    atan = wraps(math.asin)(lambda s, x: s._out(math.atan(x)))
    
    atan2 = wraps(math.atan2)(lambda s, y, x: s._out(math.atan2(y, x)))
