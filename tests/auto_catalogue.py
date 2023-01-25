'''
Not a test -- just a quick catalogue generator.
'''
import csv
import json
import toml
from datetime import datetime
from unittest import TestCase

import matplotlib.dates as mdates

from noether import catalogue


class auto_catalogue(TestCase):
    def test_autocatalogue(self):
        cat = catalogue.__json__()
        cat['$schema'] = './catalogue.schema.json'
        with open('noether/catalogue/catalogue.json', 'w') as f:
            json.dump(cat, f, indent=1)

        del cat['$schema']
        with open('noether/catalogue/catalogue.toml', 'w') as f:
            toml.dump(cat, f)

    def test_count_units(self):
        N = len(set(catalogue.units.values()))
        FMT = '%Y-%m-%d %H:%M'
        now = datetime.now().strftime(FMT)
        with open('catalogue_count.csv', 'a') as f:
            f.write(f'{now}, {N}\n')

        from matplotlib import pyplot
        with open('catalogue_count.csv') as f:
            data = [
                (datetime.strptime(date, FMT), float(N))
                for date, N in csv.reader(f)]
            print(data)
            pyplot.plot(*zip(*data))
            pyplot.title('Catalogue count')

            fig, ax = pyplot.gcf(), pyplot.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
            pyplot.xticks(rotation=90)
            fig.tight_layout()

            pyplot.savefig('catalogue_count.png')
