import noether
from noether import *

from sys import argv

print(f'{len(catalogue.units())} units, {len(list(catalogue.prefixes()))} prefixes')
print('''
>>> import noether
>>> from noether import *''')

if '--no-rich' not in argv:
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

del argv
