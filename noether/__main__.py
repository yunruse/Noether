"""
Command-line interface to Noether.

Provide terms (eg `-10degC @ degF` or `30dalton`) to see their value.

Best ran as `python -im noether`, as if no terms are provided,
a convenient interactive prompt is summoned.
"""

import noether
from noether import *


from argparse import ArgumentParser
parser = ArgumentParser(
    description=__doc__,
    usage='python -[i]m noether [-h] [--no-color] [--value] [terms ...]'
)
parser.add_argument(
    '--no-color',
    action='store_false',
    help='Suppress colour output',
    dest='color')
parser.add_argument(
    '--value', '-V',
    action='store_true',
    help='If terms are present, display only their numeric value')

# weird args like `-10degC` are thrown to `unknown`,
# but if we get args with a nargs='*', they may be in the wrong order
# therefore, we'll just fetch every unknown argument
args, unknown = parser.parse_known_args()
args.terms = unknown

pretty = None
if args.color and not args.value:
    try:
        from rich import pretty, print
    except ImportError:
        pass
    else:
        pretty.install()

if args.terms:
    from ._tokenizers import cli_dialect, transform
    src = transform(" ".join(args.terms), cli_dialect)
    try:
        del cli_dialect, transform
        value = eval(src)
        if args.value:
            if isinstance(value, Measure):
                print(value.value)
            else:
                print(value)
        else:
            print(value)
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

# TODO: allow cli dialect in the repl?

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
