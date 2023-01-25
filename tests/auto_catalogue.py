'''
Not a test -- just a quick catalogue generator.
'''
import json
import toml
from unittest import TestCase

from noether import catalogue


class test_unit_display(TestCase):
    def test_autocatalogue(self):
        cat = catalogue.__json__()
        cat['$schema'] = './catalogue.schema.json'
        with open('noether/catalogue/catalogue.json', 'w') as f:
            json.dump(cat, f, indent=1)

        del cat['$schema']
        with open('noether/catalogue/catalogue.toml', 'w') as f:
            toml.dump(cat, f)
