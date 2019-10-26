from math import log
from ..measure import Dimension, Measure
from .imperial import inch
from .fundamental import (
    U, time, length, second
)

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