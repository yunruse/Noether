"Progress of the catalogue, counted in units"

from ._helpers import TestCase, OUTPUT

import csv
from datetime import datetime

from noether import catalogue


class progress(TestCase):
    def test_count_units(self, graph=True):
        F = OUTPUT / 'catalogue_count.csv'
        F.touch()

        N = len(set(catalogue.units_by_name.values()))
        today = format(datetime.today(), '%Y-%m-%d')

        with open(F, 'a') as f:
            f.write(f'{today},{N}\n')

        if graph:
            with open(F) as f:
                # one entry per date
                data = {date: int(N) for date, N in csv.reader(f)}
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
