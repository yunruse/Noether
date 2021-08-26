# Run Noether with `python -im` for interactive console.
import noether
from noether.conf import conf_exists
from . import *
noe = noether

if not conf_exists:
    print('\n')
del conf_exists

print('''\
>>> import noether
>>> from noether import *
>>> noe = noether
''')

# TODO: if given text, output what it evaluates to
# TODO: set up syntax so, eg `4kg` -> `kg(4)`
# TODO: a `vs` operator that outputs cmp (i.e. -1, 0 or 1)
#       but reprs to something like "4 oz is bigger by 2%"
