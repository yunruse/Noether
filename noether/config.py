'''
TOML configuration.
'''

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any, Optional
import tomllib
import warnings

from .errors import ConfigWarning
from .helpers import get_dot_config

CONF_FILE = get_dot_config() / 'noether.toml'


@dataclass
class ConfigOption:
    name: str
    default: Any
    type: type
    help: str = ""

    @property
    def category(self):
        return self.name.split('_', 1)[0]

    @property
    def at_import(self):
        return self.category.isupper()


def ConfigProperty(option: ConfigOption):
    def getter(self):
        if option.name in self:
            return self[option.name]
        return option.default

    def setter(self, value):
        typ = option.type
        if not isinstance(value, typ):
            raise TypeError(
                f"conf.{option.name} must be {option.type.__name__},"
                f" not {type(value).__name__}")
        self._config[option.name] = value

        if option.at_import:
            warnings.warn(
                'This change will only apply after doing conf.save() and reloading.',
                ConfigWarning, stacklevel=2,
            )

    def deleter(self):
        if option.name in self:
            del self[option.name]
    return property(getter, setter, deleter)


class Config(dict):
    info: dict[str, ConfigOption] = dict()

    @classmethod
    def register(
        cls,
        key: str,
        default,
        help="",
        typ: Optional[type] = None,
    ):
        option = ConfigOption(
            key, default,
            typ or type(default), help
        )
        cls.info[key] = option
        setattr(cls, key, ConfigProperty(option))

    def __init__(
        self,
        value: Optional[dict] = None,
        **kwargs,
    ):
        result = {
            k: v.default
            for k, v in self.info.items()}
        result.update(value or {})
        result.update(kwargs)
        super().__init__(result)

    def __repr__(self):
        return 'Config({})'.format(', '.join(
            f'{k}={v}' for k, v in self.items()
            if v != self.info[k].default
        ))

    def get_defaults(self):
        for k in self.info:
            self.setdefault(k, self.info[k].default)

    def reset(self):
        for k in self.info:
            self[k] = self.info[k].default

    # % Attributes

    def get(self, key: str):
        if key in self:
            return self[key]
        elif key in self.info:
            return self.info[key].default
        else:
            raise KeyError('Unknown config key', key)

    # % IO

    def categories(self):
        cats: dict[str, list[str]] = dict()
        for name in sorted(self.info.keys()):
            cat, name = name.split('_', 1)
            cats.setdefault(cat, [])
            cats[cat].append(name)
        return cats

    def __str__(self, help=True):
        self.get_defaults()

        string = ""
        for cat_name, names in self.categories().items():
            string += f"\n\n[{cat_name}]"

            for name in names:
                fullname = f'{cat_name}_{name}'
                value = self.get(fullname)
                desc = self.info[fullname].help.strip()
                if help:
                    string += "\n"
                    for l in desc.split('\n'):
                        string += f'# {l}\n'
                value = json.dumps(value)
                string += f'{name} = {value}'

        return string.strip()

    def save(self, path: Path = CONF_FILE, help=True):
        os.makedirs(path.parent, exist_ok=True)
        with open(path, 'w') as f:
            f.write(self.__str__(help))

    def load(self, path: Path = CONF_FILE):
        with open(path, 'rb') as f:
            new = tomllib.load(f)

        for cat_name, cat in new.items():
            for name, value in cat.items():
                fullname = f'{cat_name}_{name}'
                if fullname in self.info:
                    self._config[fullname] = value


conf = Config()
if CONF_FILE.is_file():
    conf.load(CONF_FILE)
