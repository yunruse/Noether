from dataclasses import Field, dataclass, field

MAPPING = {
    'd': 'definition',
    'n': 'names',
    's': 'symbols',
    'k': 'kind',
    'c': 'confused_with',
    'i': 'info',
    'o': 'origin'
}


def unmap(d: dict):
    return {MAPPING.get(k, k): v for k, v in d.items()}


class NoetherYamlDict:
    __dataclass_fields__: dict[str, Field]

    def __transform(self, key: str, typ: type):
        v = getattr(self, key)
        if typ == str:
            assert isinstance(v, str)
            v = v.replace('\n', ' ')
        elif typ == list[str]:
            if isinstance(v, str):
                v = [e.strip() for e in v.split(',')]
        else:
            return
        setattr(self, key, v)

    def __post_init__(self):
        fs: dict[str, Field] = self.__dataclass_fields__
        for f, fi in fs.items():
            self.__transform(f, fi.type)


@dataclass
class UnitDef(NoetherYamlDict):
    unit: str
    names: list[str]
    symbols: list[str] = field(default_factory=list)
    kind: list[str] = field(default_factory=list)
    confused_with: list[str] = field(default_factory=list)
    info: str = ''
    origin: str = ''
    url: str = ''

    def __post_init__(self):
        super().__post_init__()
        for name in list(self.names):
            if name.startswith("'") and name.endswith("'"):
                self.names.remove(name)
                sym = name[1:-1]
                self.symbols.append(sym)


@dataclass
class UnitSetDef(NoetherYamlDict):
    unitset: str
    info: str = ''
    url: str = ''
    units: list[UnitDef] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self.unitset = self.unitset.lower().replace(' ', '_')

        self.units = [UnitDef(**unmap(d)) for d in self.units]  # type: ignore


Def = UnitDef | UnitSetDef

def Definition(d: dict) -> Def:
    d = unmap(d)
    if 'unit' in d:
        return UnitDef(**d)
    elif 'unitset' in d:
        return UnitSetDef(**d)
    else:
        raise TypeError(
            'Declaration type could not be gleaned'
            ' from keys {}'.format(
                repr(tuple(d.keys()))))
