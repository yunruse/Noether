'''
Catalogue exporter (.yaml -> _.py)
Currently in development!
'''

from argparse import ArgumentParser
from pathlib import Path
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .types import Definition


def get_definitions(path: Path):
    for noe_path in path.glob('**/*.yaml'):
        with open(noe_path) as f:
            for d in load(f, Loader):
                yield Definition(d)


parser = ArgumentParser()
parser.add_argument('root', nargs='?', default='.', type=Path)

if __name__ == '__main__':
    args = parser.parse_args()

    units = list(get_definitions(args.root))
    for u in units:
        print(u)
