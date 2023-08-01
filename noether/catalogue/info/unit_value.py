from noether.core import Measure, MeasureInfo, Unit


@Measure.Info
class info_unit_value(MeasureInfo):
    "Give unit values, rather than just the bare name."
    style = 'italic blue'

    @classmethod
    def info(cls, measure: 'Unit'):
        if isinstance(measure, Unit):
            d = measure.display_unit()
            if d is None:
                d = measure * 1
            yield d._repr_measure(measure)
