'''
Data units, including the byte, shannon and pixel.
'''

from noether.core import Unit, Dimension
from noether.core import display

from .prefixes import IEC, SI_all, SI_large
from .fundamental import length, second, time
from .scientific.cgs import cm
from .conventional import inch

from math import log


def D(d: Dimension, *n: str):
    return display(Dimension(d, *n))


time_unit = Unit(second(1024e-6), "time_unit", "TU")


# % Data

data = Dimension.new("data", "D")
linear_density = D(data / length, 'linear_density')
areal_density = D(data / length**2, 'areal_density')
volumetric_density = D(data / length**3, 'volumetric_density')
mutation_rate = D(1 / data, 'mutation_rate')
data_rate = D(data / time, 'data_rate')


bit = shannon = Unit(data, "bit", "b", SI_large | IEC)
byte = display(Unit(bit * 8, "byte", "B", SI_large | IEC))

crumb = bit * 2
nibble = Unit(bit * 4, "nibble")
base_pair = bp = Unit(bit * 2, "base_pair", "bp", SI_all)

nat = nepit = Unit(bit / log(2), 'nat')
trit = Unit(nat * log(3), 'trit')
dit = Unit(nat * log(10), ['hartley', 'ban', 'dit'], 'dit')

# % Pixels

pixel_count = Dimension.new('pixel_count', 'P')
pixel_fill_rate = D(pixel_count / time, 'pixel_fill_rate')
image_quality = D(pixel_count / length, 'image_quality')
resolution = D(pixel_count ** 2, 'resolution')
image_density = D(resolution / data, 'image_density')

pixel = dot = display(Unit(pixel_count, "pixel", "pix", SI_large))
ppi = dpi = display(Unit(pixel / inch, "ppi"))
dpcm = Unit(pixel / cm, 'dpcm')

res_480p = pixel(720) * pixel(480)
res_550p = res_1K = pixel(960) * pixel(550)
res_720p = pixel(1280) * pixel(720)
res_1080p = res_2K = pixel(1920) * pixel(1080)
res_1440p = pixel(2560) * pixel(1440)
res_2160p = res_4K = pixel(2880) * pixel(2160)
res_4320p = res_8K = pixel(7680) * pixel(4320)
