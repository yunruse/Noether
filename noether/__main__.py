"""
Command-line interface to Noether.

Provide terms (eg `-10degC @ degF` or `30dalton`) to see their value.

Best ran as `python -im noether`, as if no terms are provided,
a convenient interactive prompt is summoned.
"""

from os import environ, _exit as exit
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
    help='Suppress colour output (NO_COLOR=1 is also supported)',
    dest='color')
parser.add_argument(
    '--info',
    action='store_true',
    help='Print number of catalogue items and exit')
parser.add_argument(
    '--value', '-V',
    action='store_true',
    help='If terms are present, display only their numeric value')

# weird args like `-10degC` are thrown to `unknown`,
# but if we get args with a nargs='*', they may be in the wrong order
# therefore, we'll just fetch every unknown argument
args, unknown = parser.parse_known_args()
args.terms = unknown

# % Color

if environ.get('NO_COLOR', ''):
    args.color = False

pretty = None
if args.color and not args.value:
    try:
        from rich import pretty
    except ImportError:
        pass
    else:
        pretty.install()

# % Eval and print terms

if args.info:
    print(catalogue.info())
    exit(0)

if args.terms:
    # this is very basic at the moment!
    from ._tokenizers import units_dialect
    src = units_dialect(" ".join(args.terms))
    try:
        del units_dialect
        value = eval(src)
        if args.value:
            if isinstance(value, Measure):
                print(value.value)
            else:
                print(value)
        else:
            if isinstance(value, Measure) and pretty:
                from rich import print as _print
                _print(value)
            else:
                print(repr(value))
    except Exception as e:
        import traceback
        traceback.print_exception(e, limit=0)
        exit(2)
    else:
        exit(0)
    # regular exit(0) does not work with `python -im noether` - it displays an exception and continues.
    # _exit, meanwhile, forces an exit.
    # Note that this will NOT process any __del__ cleanups,
    # but this is considered not a major problem – bare evals automatically self-delete this way,
    # and we can't assign variables in eval(), so we shouldn't feasibly be able to, for example,
    # have `open()` leave a file handle open or something.

# % REPL

# TODO: allow cli dialect?

print(catalogue.info())
print('''
>>> import noether
>>> from noether import *''')

if pretty is not None:
    print('''\
>>> from rich import pretty
>>> pretty.install()''')
print()

del ArgumentParser, parser, args, unknown
