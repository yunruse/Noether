"Export various aspects of Noether, including its catalogue."


from ._helpers import TestCase, OUTPUT

import json
import toml

from noether import catalogue, Config


class export(TestCase):
    def test_export_config(self):
        Config().save(OUTPUT / 'default.conf')

    def test_export_catalogue(self):
        with open(OUTPUT / 'catalogue.tsv', 'w') as f:
            units = set(catalogue.units.values())
            for u in sorted(units, key=lambda u: u.name.lower()):
                chunks = [u.name, *(a for a, c in u._info())]
                print('\t'.join(chunks), file=f)

        cat = catalogue.__json__()
        cat['$schema'] = '../catalogue.schema.json'
        with open(OUTPUT / 'catalogue.json', 'w') as f:
            json.dump(cat, f, indent=1)

        del cat['$schema']
        with open(OUTPUT / 'catalogue.toml', 'w') as f:
            toml.dump(cat, f)


if __name__ == '__main__':
    export('test_count_units').test_count_units(graph=False)
