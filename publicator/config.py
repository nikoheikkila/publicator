from __future__ import annotations
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Dict, Union
import tomli

TOMLKey = str
TOMLValue = Union[str, int, float, bool, None]
Data = Dict[TOMLKey, TOMLValue]


class Configurable(metaclass=ABCMeta):
    values: Data

    @classmethod
    def from_path(self, path: Path) -> Configurable:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str, fallback: TOMLValue = None) -> TOMLValue:
        raise NotImplementedError


class Configuration(Configurable):
    def __init__(self, values: Data = {}) -> None:
        self.values = values

    @classmethod
    def from_path(cls, path: Path) -> Configurable:
        section = "tool"
        subsection = "publicator"
        items = tomli.loads(path.read_text(encoding="utf-8"))

        if section in items and subsection in items[section]:
            return cls(values=items[section][subsection])

        return NullConfiguration()

    def get(self, key: str, fallback: TOMLValue = None) -> TOMLValue:
        return self.values.get(key, fallback)


class NullConfiguration(Configurable):
    def __init__(self) -> None:
        self.values = {}

    @classmethod
    def from_path(cls, path: Path) -> Configurable:
        return cls()

    def get(self, key: str, fallback: TOMLValue = None) -> TOMLValue:
        return fallback


# Factory function
def factory(filename: str = "pyproject.toml") -> Configurable:
    path = Path.cwd() / filename

    if not path.is_file():
        return NullConfiguration()

    return Configuration.from_path(path)
