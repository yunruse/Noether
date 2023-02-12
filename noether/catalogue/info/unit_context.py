from noether.core import Measure, MeasureInfo, Unit


@Measure.Info
class info_unit_context(MeasureInfo):
    "Give additional context for units from their .info attribute."
    style = 'red underline'

    @classmethod
    def info(cls, unit: 'Unit'):
        if isinstance(unit, Unit) and unit.dim and unit.info is not None:
            yield unit.info
