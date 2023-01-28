'''
Quick analysis tools that are useful for development.

Requires matplotlib.
'''
import csv
import json
from pathlib import Path
import toml
from datetime import datetime
from unittest import TestCase

from noether import catalogue, Config

PATH = Path(__file__).parent / 'analysis'


class automation(TestCase):
    def test_export_config(self):
        Config().save(PATH / 'default.conf')

    def test_export_catalogue(self):
        with open(PATH / 'catalogue.tsv', 'w') as f:
            units = set(catalogue.units.values())
            for u in sorted(units, key=lambda u: u.name.lower()):
                chunks = [u.name, *(a for a, c in u._info())]
                print('\t'.join(chunks), file=f)

        cat = catalogue.__json__()
        cat['$schema'] = '../catalogue.schema.json'
        with open(PATH / 'catalogue.json', 'w') as f:
            json.dump(cat, f, indent=1)

        del cat['$schema']
        with open(PATH / 'catalogue.toml', 'w') as f:
            toml.dump(cat, f)

    def test_count_units(self, graph=True):
        FMT = '%Y-%m-%d'

        with open(PATH / 'catalogue_count.csv') as f:
            data = [(date, int(N)) for date, N in csv.reader(f)]

        now = datetime.now().strftime(FMT)
        N = len(set(catalogue.units.values()))
        if data[-1][0] == now:
            data[-1] = [now, N]
        else:
            data.append([now, N])

        with open(PATH / 'catalogue_count.csv', 'w') as f:
            for date, N in data:
                f.write(f'{date},{N}\n')

        if graph:
            self.graph_unit_count(data)

    def graph_unit_count(self, data):
        from matplotlib import pyplot
        import matplotlib.dates as mdates

        pyplot.plot(*zip(*data))
        pyplot.title('Catalogue count')

        fig, ax = pyplot.gcf(), pyplot.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        pyplot.xticks(rotation=90)
        fig.tight_layout()

        pyplot.savefig(PATH / 'catalogue_count.png')


if __name__ == '__main__':
    automation('test_count_units').test_count_units(graph=False)
