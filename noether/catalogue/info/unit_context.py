from ...core import Measure, MeasureInfo, Unit


@Measure.Info
class info_unit_context(MeasureInfo):
    "Give additional context for units from their .info attribute."
    style = 'red underline'

    @classmethod
    def info(self, measure: 'Unit') -> str:
        if isinstance(measure, Unit) and measure.dim and measure.info is not None:
            yield measure.info
