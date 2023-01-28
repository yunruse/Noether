from ..core.prefixes import *
from .dimensions import *

from .si import *
from .CODATA import *

from .scientific import *
from .constants import *
from .data import *

from .conventional import *
from .imperial import *

from ..config import Config, conf

Config.register('catalogue_extended', True, help='''
Provide historical, cgs, obscure and regional units. Disabling these may provide some speedup.''')

if conf.get('catalogue_extended'):
    from .extension import *

from ..core.Catalogue import Catalogue  # noqa
from . import info  # noqa

catalogue = Catalogue(locals())
