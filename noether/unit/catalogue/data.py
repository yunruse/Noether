from math import log

from ..measure import Dimension, Measure

from .fundamental import (
    U, time, length, second
)
from .conventional import cm
from .imperial import inch

## Data

data = Dimension.new(3.5, "data", "D", "B")
areal_density = data / length**2 

byte = U(data, "B", SI=True, IEC=True)
bit = shannon = U(byte / 8, "b", SI=True, IEC=True)

nat = U(bit / log(2), 'nat', SI=True)
trit = nat * log(3)
hartley = ban = dit = U(nat * log(10), 'Hart')

mutation_rate = 1 / data
base_pair = bp = U(bit * 2, "bp", SI=True)

data_rate = data / time
bps = U(bit / second, 'bps', display=True, SI=True, IEC=True)

## Pixels and printing

pixel_count = Dimension.new(3.4, "pixel_count", "P", "pix")
pixel = dot = U(pixel_count, SI=True)

pixel_fill_rate = pixel_count / time
image_density = pixel_count / data
image_quality = pixel_count / length

ppi = dpi = U(pixel / inch, 'ppi')
dpcm = U(pixel / cm, "dpcm")
