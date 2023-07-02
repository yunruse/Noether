import noether
from noether import *

#  TODO: parse e.g. `1m` -> `1 * m`?

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument(
    '--no-color',
    action='store_false',
    dest='color')  # TODO: what is the gnu standard here?
parser.add_argument('terms', nargs='*')

args = parser.parse_args()

if args.terms:
    # this is very basic at the moment!
    __terms = " ".join(args.terms)
    del args, parser, ArgumentParser
    print(eval(__terms))

    # regular exit(0) does not work with `python -im noether` - it displays an exception and continues.
    # _exit, meanwhile, forces an exit.
    # Note that this will NOT process any __del__ cleanups,
    # but this is considered not a major problem – bare evals automatically self-delete this way,
    # and we can't assign variables in eval(), so we shouldn't feasibly be able to, for example,
    # have `open()` leave a file handle open or something.
    import os
    os._exit(0)

print(f'{len(catalogue.units())} units, {len(list(catalogue.prefixes()))} prefixes')
print('''
>>> import noether
>>> from noether import *''')

if args.color:
    try:
        from rich import pretty, print
    except ImportError:
        pass
    else:
        pretty.install()
        print('''\
>>> from rich import pretty, print
>>> pretty.install()''')
print()

del args, parser, ArgumentParser
