"""
Conversion calculator with multilicative and affine scales.

If provided with a term ('terminal mode'), outputs its value.
Otherwise launches an interactive REPL for working with units, near-identical to Python.

Terms might be provided in such a way as:

$ uvx noether lunation
lunation  # time, 29 d + 12 hr + 44 min + 2.9 s, Average time between moon phases; mean orbital period wrt sol-earth line.

$ uvx noether -V 30dalton @ picogram
4.981617e-11

This command is equivalent to running Python's REPL with the header

>>> import noether as noe
>>> from noether import *

In addition a syntax dialect is enabled allowing function postfixes to numbers.
For example, `-10degC` is interpreted as `degC(-10)`.

In terminal mode, for convenience,
 `x`, `^` and `in` are allowable substitutes for `*`, `**` and `inch`.
"""

SHORTHAND_HELP = """
terms may be provided like
    30pg @ dalton
    80in / year^2
    solar_mass @ Yg
    8cm x 40cm
"""

from os import environ
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from tokenize import TokenError

import noether as noe
from noether._tokenizers import cli_dialect, transform


def namespace():
    # import noether as noe
    # from noether import *
    namespace = {}
    namespace['noe'] = noe
    namespace.update(noe.__dict__)
    return namespace


parser = ArgumentParser(
    description=__doc__,
    formatter_class=RawDescriptionHelpFormatter,
    usage='python -[i]m noether [-h|--help] [--no-color] [--value] [terms ...]',
    add_help=False,
)
parser.add_argument(
    '-h', dest="short_help",
    action='store_true',
    help='show short help message')
parser.add_argument(
    '--help', dest="long_help",
    action='store_true',
    help='show long help message')
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
    '--value', '-v',
    action='store_true',
    help='If terms are present, display only their numeric value. If a unit is not requested it is assumed SI.')


def repl():
    "Console REPL if called with no arguments. Runs in cli_dialect"

    from code import interact as _pyrepl
    banner = noe.catalogue.info()

    import readline  # necessary for arrow-key functionality
    def readfunc(prompt: str):
        try:
            text = input(prompt)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            return ""
        try:
            return transform(text, cli_dialect, pythonesque=True)
        except TokenError as te:
            if te.args[0] != 'EOF in multi-line statement':
                print("TokenError: EOF in multi-line statement (currently not supported)")
                return ""
                # TODO: support multi-line statements custom interpreter?
            else:
                raise
    
    _pyrepl(banner, readfunc, namespace(), exitmsg="")

def main():
    # weird args like `-10degC` are thrown to `unknown`,
    # but if we get args with a nargs='*', they may be in the wrong order
    # therefore, we'll just fetch every unknown argument
    args, unknown = parser.parse_known_args()
    args.terms = unknown

    if args.long_help:
        parser.print_help()
        exit(0)
    if args.short_help:
        parser.print_usage()
        print(SHORTHAND_HELP)
        exit(0)

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
        print(noe.catalogue.info())
        exit(0)

    if args.terms:
        src = transform(" ".join(args.terms), cli_dialect, pythonesque=False)
        try:
            value = eval(src, namespace())
            if args.value:
                if isinstance(value, noe.Measure):
                    print(value.value)
                else:
                    print(value)
            else:
                if isinstance(value, noe.Measure) and pretty:
                    from rich import print as _print
                    _print(value)
                else:
                    print(repr(value))
        except Exception as e:
            import traceback
            traceback.print_exception(e, limit=0)
            exit(2)

        exit(0)
    
    else:
        # No terms; implied repl
        repl()
