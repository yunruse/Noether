from typing import Generator

from math import log

from noether import Dimension, Measure, MeasureInfo

from .. import angstrom, km, cm, meter, foot
from .. import year, day, hour, minute, second
from .. import c

# TODO: incorporate all catalogue units to save effort
# and then you can move some unusual units to a new `unusual.py`

kmq = km**2
COMPARISON_MEASURES: dict[str, Measure] = {
    'average human height': cm(170),

    'a light-minute': c * minute,
    'a light-second': c * second,
    'a light-nanosecond': c * second * 1e-9,

    'the length of horse': meter(2.4),
    'a city block': meter(100),

    'the length of a double-decker bus': meter(18.75),

    'the length of a football field': meter(104),
    'the length of an American football field': foot(360),

    # % Area

    'a football field': meter(104) * meter(68),
    'an American football field': foot(360) * foot(160),

    'Wales': kmq(20_779),
    'Isle of Wight': kmq(380),

    'Rhode Island': kmq(4_000),
    'Texas': kmq(695_670),
    'Alaska': kmq(1_700_130),

    'Belgium': kmq(30_528),
    'Saarland': kmq(2_569.69),

    'Sergipe': kmq(91_910.4),
    'São Paulo': kmq(1_521.11),

    # % Speed
    'the speed of sound in air': meter(343) / second,
    'average human walk speed': meter(1.42) / second,
}


@Measure.Info
class info_comparison(MeasureInfo):
    "Compare measures to everyday or well-known items."
    style = 'underline red'
    enabled_by_default = False  # per #17, needs some tweaks to be considered "good enough"

    @classmethod
    def units(cls, dim: Dimension):
        for k, v in COMPARISON_MEASURES.items():
            if v.dim == dim:
                yield k, v

        from noether import catalogue

        for unit in catalogue.units_by_dimension.get(dim, []):
            yield unit.name, unit

    @classmethod
    def get_comparisons(cls, measure: Measure):
        """
        Return comparisons with "scores".
        Scores are related to how close a comparison is to the measure,
        but boosted for those of the target country.
        """
        for name, unit in cls.units(measure.dim):

            score = -abs(log(measure / unit))
            if score == 0:
                continue  # ignore units that are identical
            yield score, name, unit

    @classmethod
    def info(cls, measure: Measure):
        comparisons = list(cls.get_comparisons(measure))
        if not comparisons:
            return
        best_score, name, unit = max(comparisons, key=lambda x: x[0])
        relative = float(measure / unit)
        yield f'{relative:.2f}× {name}'
