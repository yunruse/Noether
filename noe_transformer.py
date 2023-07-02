'''
Internal tool for catalogue generation.
Transforms `.units.py` files to `_.py` files.

Many unit definitions are slightly unwieldy,
especially in the repetition of names.
As such, this transpiles some shorthand syntax.

While the regular expression has been tested,
you should still make sure to run unit tests.
'''

# TODO: As a long term goal it would be wonderful
# to leverage this format, a strict subset of Python syntax (cf CONTRIBUTING.md)
# to be:
# - used in the *entirety* of the catalogue
# - formalised in format
# - capable of rendering to JSON, including symbolic relationships AND actual values
# - render an entire catalogue in one Python file
# - based on configuration (how?) also generate all prefixed units, for better linting...???

from pathlib import Path
from re import compile, MULTILINE, IGNORECASE, VERBOSE
from argparse import ArgumentParser
from typing import Callable

# TODO: regex is not the wisest.
# Really, consider using python's `tokenize`.

UNIT_MATCH = compile(r'''
^(?P<targets>.+?)\s*=\s*
\s* (?P<expr>[a-z_0-9\.\/* ]+)
\n \# \s* (?P<info>.+) \n
''', MULTILINE | IGNORECASE | VERBOSE)

UNIT_FMT = """\
{targets} = Unit(
    {expr},
    [{names}]{symbols},
    info={info!r})
"""

HEADER = '''\
# This file was autogenerated from a .units.py file
# via `make units`
'''


def transmogrify_shorthand(text: str):
    unit_matches = UNIT_MATCH.finditer(text)

    new_text = HEADER
    last_index = 0
    for match in unit_matches:
        new_text += text[last_index:match.start()]

        g = match.groupdict()
        names = []
        symbols = []
        for n in g['targets'].split(' = '):
            if n.startswith("'") and n.endswith("'"):
                symbols.append(n)
            else:
                names.append(n)

        g['names'] = ', '.join(map(repr, names))
        g['symbols'] = ''
        if symbols:
            g['symbols'] = ', ' + '[{}]'.format(', '.join(symbols))
        g['targets'] = ' = '.join(names)
        new_text += UNIT_FMT.format(**g)

        last_index = match.end()

    new_text += text[last_index:]

    return new_text
    # MAIN_FIND matchall
    # for each match
    # names = ', '.join(map(repr, names))
    # substitute MAIN_REPL


def transform_file(pi: Path, po: Path, f: Callable[[str], str]):
    with open(pi, 'r') as fi:
        with open(po, 'w') as fo:
            fo.write(f(fi.read()))


parser = ArgumentParser()
parser.add_argument('root', nargs='?', default='.', type=Path)
parser.add_argument('--remove', action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()
    for noe_path in args.root.glob('**/*.units.py'):
        export_path = Path(str(noe_path).removesuffix('.units.py') + '_.py')
        if args.remove:
            print('deleting', export_path)
            export_path.unlink(missing_ok=True)
        else:
            print('exporting', export_path)
            transform_file(noe_path, export_path, transmogrify_shorthand)
