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

Config.register('CATALOGUE_extended', True, help='''\
Provide historical, obscure and regional units.''')
if conf.get('CATALOGUE_extended'):
    from .extension import *

Config.register('CATALOGUE_fun', True, help='''\
Provide humorous and fictional units of measure.''')
if conf.get('CATALOGUE_fun'):
    from .humorous import *

from ..core.Catalogue import Catalogue  # noqa
from . import info  # noqa

catalogue = Catalogue(locals())

Config.register('CATALOGUE_all_prefixes_in_namespace', True, help='''\
Put every prefixed unit (microohm, kibibyte &c) as measures in the Noether namespace.
This may cause annoyance if you `from noether import *`!''')
if conf.get('CATALOGUE_all_prefixes_in_namespace'):
    vars().update(catalogue.all_units)
