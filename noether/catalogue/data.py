'''
Data units, including the byte, shannon and pixel.
'''

from ..core import Unit, Dimension
from ..core.Prefix import IEC, SI, SI_large
from ..core.DisplaySet import display as I

from noether.core.fundamental import length, second, time
from .conventional import cm
from .imperial import inch

from math import log


time_unit = Unit(second(1024e-6), "time_unit", "TU")


# % Data

data = Dimension.new("data", "D")
linear_density = I(data / length, 'linear_density')
areal_density = I(data / length**2, 'areal_density')
volumetric_density = I(data / length**3, 'volumetric_density')
mutation_rate = I(1 / data, 'mutation_rate')
data_rate = I(data / time, 'data_rate')


bit = shannon = Unit(data, "bit", "b", SI_large+IEC)
byte = I(Unit(bit * 8, "byte", "B", SI_large+IEC))

crumb = bit * 2
nibble = Unit(bit * 4, "nibble")
base_pair = bp = Unit(bit * 2, "base_pair", "bp", SI)

nat = nepit = Unit(bit / log(2), 'nat')
trit = Unit(nat * log(3), 'trit')
dit = Unit(nat * log(10), ['hartley', 'ban', 'dit'], 'dit')

# % Pixels

pixel_count = Dimension.new('pixel_count', 'P')
pixel_fill_rate = I(pixel_count / time, 'pixel_fill_rate')
image_quality = I(pixel_count / length, 'image_quality')
resolution = I(pixel_count ** 2, 'resolution')
image_density = I(resolution / data, 'image_density')

pixel = dot = I(Unit(pixel_count, "pixel", "pix", SI_large))
ppi = dpi = I(Unit(pixel / inch, "ppi"))
dpcm = Unit(pixel / cm, 'dpcm')

res_480p = pixel(720) * pixel(480)
res_550p = res_1K = pixel(960) * pixel(550)
res_720p = pixel(1280) * pixel(720)
res_1080p = res_2K = pixel(1920) * pixel(1080)
res_1440p = pixel(2560) * pixel(1440)
res_2160p = res_4K = pixel(2880) * pixel(2160)
res_4320p = res_8K = pixel(7680) * pixel(4320)
