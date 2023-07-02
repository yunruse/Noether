"""
TODO: write a description here...
"""

import noether
from noether import *

#  TODO: parse e.g. `1m` -> `1 * m`?

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument(
    '--no-color',  # TODO: what is the gnu standard here?
    action='store_false',
    help='Suppress colour output',
    dest='color')
parser.add_argument(
    '--value', '-V',  # TODO: what is the gnu standard here?
    action='store_true',
    help='Display the value only (equivalent to str(statement))')

# TODO: add --si

parser.add_argument('terms', nargs='*')

args = parser.parse_args()

pretty = None
if args.color and not args.value:
    try:
        from rich import pretty, print
    except ImportError:
        pass
    else:
        pretty.install()

if args.terms:
    # this is very basic at the moment!
    import os
    try:
        value = eval(" ".join(args.terms))
        if args.value:
            print(value)
        else:
            print(repr(value))
    except Exception as e:
        import traceback
        traceback.print_exception(e, limit=0)
        import os
        os._exit(2)
    else:
        import os
        os._exit(0)
    # regular exit(0) does not work with `python -im noether` - it displays an exception and continues.
    # _exit, meanwhile, forces an exit.
    # Note that this will NOT process any __del__ cleanups,
    # but this is considered not a major problem – bare evals automatically self-delete this way,
    # and we can't assign variables in eval(), so we shouldn't feasibly be able to, for example,
    # have `open()` leave a file handle open or something.

print(f'{len(catalogue.units())} units, {len(list(catalogue.prefixes()))} prefixes')
print('''
>>> import noether
>>> from noether import *''')

if pretty is not None:
    print('''\
>>> from rich import pretty, print
>>> pretty.install()''')
print()

del args, parser, ArgumentParser
