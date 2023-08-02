from noether.core import Measure, MeasureInfo, MeasureRelative, Unit, LogarithmicUnit


@Measure.Info
class info_unit_value(MeasureInfo):
    "Give unit values, rather than just the bare name."
    style = 'italic blue'

    @classmethod
    def info(cls, measure: Measure):
        if isinstance(measure, Unit):
            d = measure.display_unit()
            if d is None:
                d = measure * 1
            yield d._repr_measure(measure)
        if isinstance(measure, MeasureRelative) and isinstance(measure.unit, LogarithmicUnit):
            underlying_unit = measure.unit.unit
            if not isinstance(underlying_unit, Unit):
                underlying_unit = Measure(underlying_unit).display_unit()
            yield underlying_unit._repr_measure(measure)
