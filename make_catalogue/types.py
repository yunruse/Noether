from dataclasses import Field, dataclass, field

from noether._tokenizers import units_dialect

from noether.Multiplication import Multiplication

MAPPING = {
    'd': 'definition',
    'n': 'names',
    's': 'symbols',
    'p': 'prefixes',
    'c': 'confused_with',
    'i': 'info',
    'o': 'origin',
}


def unmap(d: dict):
    return {MAPPING.get(k, k): v for k, v in d.items()}


class CatalogueDef:
    '''
    A catalogue definition.

    Provides some string manipulation on dataclasses.
    '''
    __dataclass_fields__: dict[str, Field]

    def __transform(self, key: str, typ: type):
        v = getattr(self, key)
        if typ == str:
            v = str(v).replace('\n', ' ').strip()
        elif typ == list[str]:
            if isinstance(v, str):
                v = [e.strip() for e in v.split(',')]
        else:
            return
        setattr(self, key, v)

    def __post_init__(self):
        for f, fi in self.__dataclass_fields__.items():
            if fi.init:
                self.__transform(f, fi.type)


@dataclass
class BaseDimensionDef(CatalogueDef):
    basedimension: str  # name
    symbol: str


@dataclass
class DimensionDef(CatalogueDef):
    dimension: str  # value
    names: list[str]

    # derived:
    value: Multiplication[str] = field(init=False, repr=False)


@dataclass
class PrefixDef(CatalogueDef):
    prefix: str
    symbol: str
    value: float | int


@dataclass
class PrefixSetDef(CatalogueDef):
    prefixset: str
    includes: list[str] = field(default_factory=list)
    prefixes: list[PrefixDef] = field(default_factory=list)

    # derived:
    names: list[str] = field(init=False, repr=False)

    def __post_init__(self):
        super().__post_init__()

        self.prefixes = [
            PrefixDef(**unmap(d)) for d in self.prefixes]  # type: ignore


@dataclass
class UnitDef(CatalogueDef):
    unit: str
    names: list[str]
    symbols: list[str] = field(default_factory=list)
    unit_sets: list[str] = field(default_factory=list)
    prefixes: str = ''
    confused_with: list[str] = field(default_factory=list)
    info: str = ''
    origin: str = ''
    url: str = ''

    def __post_init__(self):
        super().__post_init__()

        self.unit = units_dialect(self.unit)

        for name in list(self.names):
            if name.startswith("'") and name.endswith("'"):
                self.names.remove(name)
                sym = name[1:-1]
                self.symbols.append(sym)


@dataclass
class UnitSetDef(CatalogueDef):
    unitset: str
    info: str = ''
    url: str = ''
    units: list[UnitDef] = field(default_factory=list)

    # derived:
    names: list[str] = field(init=False, repr=False)

    def __post_init__(self):
        super().__post_init__()
        self.unitset = self.unitset.lower().replace(' ', '_')

        self.units = [UnitDef(**unmap(d)) for d in self.units]  # type: ignore


def Definition(d: dict) -> CatalogueDef:
    d = unmap(d)
    if 'prefix' in d:
        return PrefixDef(**d)
    if 'prefixset' in d:
        return PrefixSetDef(**d)
    if 'basedimension' in d:
        return BaseDimensionDef(**d)
    if 'dimension' in d:
        return DimensionDef(**d)
    if 'unit' in d:
        return UnitDef(**d)
    if 'unitset' in d:
        return UnitSetDef(**d)
    raise TypeError(
        'Declaration type could not be gleaned'
        ' from keys {}'.format(
            repr(tuple(d.keys()))))
