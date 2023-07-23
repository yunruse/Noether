'''
TOML configuration.
'''

from typing import Generic, TypeVar
from dataclasses import dataclass

import json
import os
from pathlib import Path
import toml
import warnings

from .errors import ConfigWarning
from .helpers import get_dot_config

CONF_FILE = get_dot_config() / 'noether.toml'

ConfigType = TypeVar('ConfigType', bool, str, int)


@dataclass
class ConfigOption(Generic[ConfigType]):
    name: str
    default: ConfigType
    type: type
    help: str = ""

    @property
    def category(self):
        return self.name.split('_', 1)[0]

    @property
    def at_import(self):
        return self.category.isupper()


def ConfigProperty(option: ConfigOption):
    def getter(self: Config):
        if option.name in self._config:
            return self._config[option.name]
        return option.default

    def setter(self: Config, value):
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

    def deleter(self: Config):
        if option.name in self._config:
            del self._config[option.name]
    return property(getter, setter, deleter)


class Config:
    _config: dict
    options: dict[str, ConfigOption] = dict()

    @classmethod
    def register(
        cls,
        key: str,
        default: ConfigType,
        help: str | None = None,
        typ: type | None = None,
    ):
        option = ConfigOption(
            key, default,
            typ or type(default), help or ""
        )
        cls.options[key] = option
        setattr(cls, key, ConfigProperty(option))
        return key

    def __init__(
        self,
        value: dict | None = None,
        **kwargs,
    ):
        self._config = {
            k: v.default
            for k, v in self.options.items()}
        self._config.update(value or {})
        self._config.update(kwargs)

    def _show_in_repr(self, k: str, v):
        if k not in self.options:
            return True
        return bool(v != self.options[k].default)

    def __repr__(self):
        return 'Config({})'.format(', '.join(
            f'{k}={v}' for k, v in self._config.items()
            if self._show_in_repr(k, v)
        ))

    def _get_defaults(self):
        for k in self.options:
            self._config.setdefault(k, self.options[k].default)

    def reset(self):
        for k in self.options:
            self._config[k] = self.options[k].default

    # % Attributes

    def get(self, key: str):
        if key in self._config:
            return self._config[key]
        elif key in self.options:
            return self.options[key].default
        else:
            raise KeyError('Unknown config key', key)

    # % IO

    def categories(self):
        cats: dict[str, list[str]] = dict()
        for name in sorted(self.options.keys()):
            cat, name = name.split('_', 1)
            cats.setdefault(cat, [])
            cats[cat].append(name)
        return cats

    def __str__(self, help=True):
        self._get_defaults()

        string = ""
        for cat_name, names in self.categories().items():
            string += f"\n\n[{cat_name}]"

            for name in names:
                fullname = f'{cat_name}_{name}'
                value = self.get(fullname)
                desc = self.options[fullname].help.strip()
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

    def _load(self, path: Path = CONF_FILE):
        with open(path) as f:
            new = toml.load(f)

        for cat_name, cat in new.items():
            for name, value in cat.items():
                fullname = f'{cat_name}_{name}'
                self._config[fullname] = value

    def _remove_unused_keys(self):
        for name in list(self._config):
            if name not in self.options:
                warnings.warn(
                    f"Unknown config option {name!r}.",
                    ConfigWarning, stacklevel=4
                )
                del self._config[name]

    def load(self, path: Path = CONF_FILE):
        self._load(path)
        self._remove_unused_keys()


conf = Config()
if CONF_FILE.is_file():
    conf._load(CONF_FILE)
