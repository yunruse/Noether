import noether
from noether import *

from sys import argv

print(f'{catalogue.unit_count()} units, {catalogue.prefix_count()} prefixes')
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
