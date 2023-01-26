'''
Units used primarily by ancient Israelites.
'''

from ....core.fundamental import meter
from ....core import Unit

# % Length
shaku = 尺 = Unit(meter * 0.303, '尺')

sun = 寸 = Unit(尺 / 10, '寸')
bu = 分 = Unit(尺 / 100, '分')
rin = 厘 = 釐 = Unit(尺 / 1000, ['厘', '釐'])
mou = mo = mō = 毛 = 毫 = Unit(尺 / 10_000, ['毛', '毫'])

ken = hiro = 間 = 尋 = Unit(尺 * 6, ['間', '尋'])
jou = jō = 丈 = Unit(尺 * 10, '丈')
chou = chō = 町 = Unit(尺 * 360, '町')
ri = 里 = Unit(尺 * 12_96, '町')

# % Area
tsubo = bu = 坪 = 歩 = Unit(間**2, ['坪', '歩'])

畳 = Unit(坪 / 2, '畳')
合 = Unit(坪 / 10, '合')
勺 = Unit(坪 / 100, '勺')

se = 畝 = Unit(坪 * 30, '畝')
tan = 段 = 反 = Unit(坪 * 300, ['段', '反'])
町 = Unit(坪 * 3000, '畝')

# TODO: https://en.wikipedia.org/wiki/Japanese_units_of_measurement#Volume
