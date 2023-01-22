import noether
from noether import *

print('''\
>>> import noether
>>> from noether.import *''')

try:
    from rich import pretty, print
except ImportError:
    pretty = None
else:
    pretty.install()
    print('''\
>>> from rich import pretty, print
>>> pretty.install()''')
print()

# TODO: fancy repl
