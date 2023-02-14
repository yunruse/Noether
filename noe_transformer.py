'''
Many unit definitions are slightly unwieldy,
especially in the repetition of names.

As such, this transformer takes .noe.py files and
autogenerates equivalent .py files by transpiling a
bit of shorthand syntax, so adding units to the
catalogue is less of a nightmare.

While the regular expression has been tested,
you should still run `python -m noether` just in case.
'''

from pathlib import Path
from re import compile, MULTILINE, IGNORECASE, VERBOSE
from argparse import ArgumentParser
from typing import Callable

UNIT_MATCH = compile(r'''
^(?P<targets>.+?)\s*=\s*
\s* (?P<expr>[a-z_0-9\.\/* ]+)
\n \# \s* (?P<info>.+) \n
''', MULTILINE | IGNORECASE | VERBOSE)

UNIT_FMT = """\
{targets} = Unit(
    {expr},
    [{names}],
    info={info!r})
"""

HEADER = '''\
# This file was autogenerated from a .noe.py file
# (via noe_transformer.py).
# It is not the source document.
'''


def transmogrify_shorthand(text: str):
    unit_matches = UNIT_MATCH.finditer(text)

    new_text = HEADER
    last_index = 0
    for match in unit_matches:
        new_text += text[last_index:match.start()]

        g = match.groupdict()
        g['names'] = ', '.join(map(repr, g['targets'].split(' = ')))
        new_text += UNIT_FMT.format(**g)

        last_index = match.end()

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
    for noe_path in args.root.glob('**/*.noe.py'):
        export_path = Path(str(noe_path).removesuffix('.noe.py') + '.py')
        if args.remove:
            print('deleting', export_path)
            export_path.unlink(missing_ok=True)
        else:
            print('exporting', export_path)
            transform_file(noe_path, export_path, transmogrify_shorthand)
