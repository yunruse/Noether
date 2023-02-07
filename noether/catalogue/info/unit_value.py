from ...core import Measure, MeasureInfo, Unit


@Measure.Info
class info_unit_value(MeasureInfo):
    "Give unit values, rather than just the bare name."
    style = 'italic blue'

    @classmethod
    def info(self, measure: 'Unit') -> str:
        if isinstance(measure, Unit) and measure.dim:

            d = measure.display_unit()
            if d != measure:
                if d is None:
                    d = measure * 1
                yield d.repr_measure(measure)
