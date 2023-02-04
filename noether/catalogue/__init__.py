from noether.core.Prefix import *
from noether.config import Config, conf

# Dimensions
from .dimensions import *

# Units are imported in this exact order
from .scientific import *

from .conventional import *

Config.register('CATALOGUE_historical', True, help='''\
Provide historical units.''')
if conf.get('CATALOGUE_historical'):
    from .extension import *

Config.register('CATALOGUE_humorous', True, help='''\
Provide humorous and fictional units.''')
if conf.get('CATALOGUE_humorous'):
    from .humorous import *

# Catalogue export

from ..core.Catalogue import Catalogue  # noqa
from . import info  # noqa

catalogue = Catalogue(locals())

vars().update({p.prefix: p for p in catalogue.prefixes})

Config.register('CATALOGUE_all_prefixes_in_namespace', True, help='''\
Put every prefixed unit (microohm, kibibyte &c) as measures in the Noether namespace.
This may cause annoyance if you `from noether import *`!''')
if conf.get('CATALOGUE_all_prefixes_in_namespace'):
    vars().update(catalogue.all_prefixed_units)
