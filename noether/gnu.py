'''
A GNU Units-like CLI. Note that the `-f` option is not currently supported.

See `man units` for info on usage.
'''

from argparse import ArgumentParser

from noether import catalogue, conf, Measure, Prefix, dimensionless

from noether.display import DISPLAY_DIGITS, DISPLAY_UNDERSCORE_AFTER

parser = ArgumentParser(
    description=__doc__,
    usage='units [-q] [from-unit to-unit]'
)

parser.add_argument(
    'units', nargs='*',
    help='Allow a single units conversion; prompts are not printed.')
parser.add_argument(
    '-q', action='store_false', dest='loud',
    help='Suppress prompts in interactive mode.')

Value = Measure | Prefix

# conf._config[DISPLAY_DIGITS] = 4
# conf._config[DISPLAY_UNDERSCORE_AFTER] = -1


def dim(v: Value):
    if isinstance(v, Prefix):
        return dimensionless
    return v.dim


def compare(a: Value, b: Value):
    if dim(a) != dim(b):
        print('conformability error')
        print(' '*7, a)
        print(' '*7, b)

    print(' '*7, '*', (a/b).value)
    print(' '*7, '/', (b/a).value)


def get(inp: str) -> Value | None:
    try:
        unit = catalogue.get(inp)
    except NameError:
        print(f"unknown unit '{inp}'")
    else:
        if not isinstance(unit, (Measure, Prefix)):
            print(f"unknown unit '{inp}'")
        else:
            return unit


def prompt(prompt: str) -> Value:
    while True:
        unit = get(input(prompt))
        if unit is not None:
            return unit


if __name__ == '__main__':
    args = parser.parse_args()

    if args.units:
        if len(args.units) != 2:
            parser.print_usage()
            parser.exit(2)
        a, b = args.units
        compare(get(a) or exit(2), get(b) or exit(2))
        exit(0)

    if args.loud:
        U = len(catalogue.units())
        P = len(list(catalogue.prefixes()))
        print(f'{U} units, {P} prefixes')

    have = 'You have: ' * args.loud
    want = 'You want: ' * args.loud
    try:
        while True:
            compare(prompt(have), prompt(want))
    except KeyboardInterrupt:
        exit(130)
