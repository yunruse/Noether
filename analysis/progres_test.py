"Progress of the catalogue, counted in units"

from ._helpers import TestCase, OUTPUT

import csv
from datetime import datetime

from noether import catalogue


class progress(TestCase):
    def test_count_units(self, graph=True):
        FMT = '%Y-%m-%d'

        with open(OUTPUT / 'catalogue_count.csv') as f:
            data = [(date, int(N)) for date, N in csv.reader(f)]

        now = datetime.now().strftime(FMT)
        N = len(set(catalogue.units.values()))
        if data[-1][0] == now:
            data[-1] = [now, N]
        else:
            data.append([now, N])

        with open(OUTPUT / 'catalogue_count.csv', 'w') as f:
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

        pyplot.savefig(OUTPUT / 'catalogue_count.png')


if __name__ == '__main__':
    progress('test_count_units').test_count_units(graph=False)
