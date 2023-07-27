'''
Catalogue exporter (.yaml -> _.py)
Currently in development!
'''

from argparse import ArgumentParser
from pathlib import Path

from .catalogue import Catalogue


parser = ArgumentParser()
parser.add_argument(
    'root', nargs='?', type=Path,
    default='.')
parser.add_argument(
    'export_path', nargs='?', type=Path,
    default='./noether/catalogue.py')

if __name__ == '__main__':
    args = parser.parse_args()

    units = Catalogue.from_path(args.root)

    with open(args.export_path, 'w') as f:
        f.write(units.render())
