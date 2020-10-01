from math import log

from ..measure import Dimension, Measure

from .fundamental import (
    U, time, length, second
)
from .conventional import cm
from .imperial import inch

# # Data

data = Dimension.new("data", dimsym="D", unitsym="B", order=500)
areal_density = data / length**2

byte = U(data, "B", SI=True, pIEC=True)
bit = shannon = U(byte / 8, "b", SI=True, pIEC=True)

nat = U(bit / log(2), 'nat', SI=True)
trit = nat * log(3)
hartley = ban = dit = U(nat * log(10), 'Hart')

mutation_rate = 1 / data
base_pair = bp = U(bit * 2, "bp", SI=True)

data_rate = data / time
bps = U(bit / second, 'bps', display=True, SI=True, pIEC=True)

# # Pixels and printing

pixel_count = Dimension.new(
    "pixel_count", dimsym="P", unitsym="pix", order=400)
pixel = dot = U(pixel_count, pSIb=True)

pixel_fill_rate = pixel_count / time
image_density = pixel_count / data
image_quality = pixel_count / length

ppi = dpi = U(pixel / inch, 'ppi')
dpcm = U(pixel / cm, "dpcm")

res_480p = pixel(720) * pixel(480)
res_550p = res_1K = pixel(960) * pixel(550)
res_720p = pixel(1280) * pixel(720)
res_1080p = res_2K = pixel(1920) * pixel(1080)
res_1440p = pixel(2560) * pixel(1440)
res_2160p = res_4K = pixel(2880) * pixel(2160)
res_4320p = res_8K = pixel(7680) * pixel(4320)
