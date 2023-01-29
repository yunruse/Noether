from ...core import Measure, MeasureInfo


@Measure.Info
class info_dimension(MeasureInfo):
    "Display the dimension of a measure."
    style = 'green italic'

    @classmethod
    def info(self, measure: Measure):
        yield measure.dim.canonical_name()
