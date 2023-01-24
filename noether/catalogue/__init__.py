from .dimensions import *
from .si import *

from .constants import *
from .scientific import *
from .data import *

from .conventional import *
from .imperial import *

from ..core.config import Config, conf

Config.register('catalogue_extended', True, help='''
Provide historical, cgs, obscure and regional units. Disabling these may provide some speedup.''')

if conf.get('catalogue_extended'):
    from .extension import *
