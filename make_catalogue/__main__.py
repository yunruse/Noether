'''
Catalogue exporter (.yaml -> _.py)
Currently in development!
'''

from argparse import ArgumentParser
from pathlib import Path
import json

import yaml

from .catalogue import Catalogue


parser = ArgumentParser()
parser.add_argument(
    'root', nargs='?', type=Path,
    default='.')
parser.add_argument('--json', type=Path)
parser.add_argument('--yaml', type=Path)
parser.add_argument('--python', type=Path)


def get_definitions(path: Path):
    for noe_path in path.glob('**/*.yaml'):
        with open(noe_path) as f:
            yield from yaml.load(f, yaml.Loader)


if __name__ == '__main__':
    args = parser.parse_args()

    defs = list(get_definitions(args.root))

    # TODO: better json/yaml export mechanism..?

    if args.json:
        with open(args.json, 'w') as f:
            json.dump(defs, f)

    if args.yaml:
        with open(args.yaml, 'w') as f:
            yaml.dump(defs, f)

    if args.python:
        catalogue = Catalogue(defs)
        with open(args.python, 'w') as f:
            f.write(catalogue.render())
