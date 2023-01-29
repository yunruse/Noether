from typing import Generator, TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from .Measure import Measure


class MeasureInfo:
    '''Handler for display of Measures.'''
    @classmethod
    def info(cls, measure: 'Measure') -> Generator[str, None, None]:
        return NotImplemented

    @classmethod
    def should_display(cls, measure: 'Measure') -> bool:
        return True

    enabled_by_default: ClassVar[bool] = True
    style: ClassVar[str] = 'purple italic'
