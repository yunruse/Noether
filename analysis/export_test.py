"Export various aspects of Noether, including its catalogue."


from typing import Any
from ._helpers import TestCase, OUTPUT

import json
import toml

from noether import catalogue, Config


class export(TestCase):
    def test_export_config(self):
        Config().save(OUTPUT / 'default.conf')

    def test_export_catalogue(self):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT / 'catalogue.tsv', 'w') as f:
            units = set(catalogue.units_by_name.values())
            for u in sorted(units, key=lambda u: u.name.lower()):
                chunks = [u.name, *(a for a, c in u._info())]
                print('\t'.join(chunks), file=f)

        cat: dict[str, Any] = catalogue.__json__()
        cat['$schema'] = '../catalogue.schema.json'
        with open(OUTPUT / 'catalogue.json', 'w') as f:
            json.dump(cat, f, indent=1)

        del cat['$schema']
        with open(OUTPUT / 'catalogue.toml', 'w') as f:
            toml.dump(cat, f)
