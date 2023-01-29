from ..core.Prefix import *
from .dimensions import *

from .si import *
from .CODATA import *

from .scientific import *
from .constants import *
from .data import *

from .conventional import *
from .cgs import *
from .imperial import *

from ..config import Config, conf

Config.register('CATALOGUE_extended', True, help='''
Provide historical, cgs, obscure and regional units. Disabling these may provide some speedup.''')

if conf.get('CATALOGUE_extended'):
    from .extension import *

from ..core.Catalogue import Catalogue  # noqa
from . import info  # noqa

catalogue = Catalogue(locals())
