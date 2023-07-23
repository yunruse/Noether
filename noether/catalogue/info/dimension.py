from noether.core import Measure, MeasureInfo


@Measure.Info
class info_dimension(MeasureInfo):
    "Display the dimension of a measure."
    style = 'green italic'

    @classmethod
    def info(cls, measure: Measure):
        if measure.dim:
            yield measure.dim.name()
