from __future__ import annotations
from dataclasses import dataclass
from unittest.mock import patch

@dataclass(frozen=True)
class Semver():
    major: int = 0
    minor: int = 1
    patch: int = 0

    @classmethod
    def from_string(self, version: str) -> Semver:
        major, minor, patch = map(int, version.split('.'))
        return Semver(major, minor, patch)

    def as_tuple(self) -> tuple[int]:
        return (self.major, self.minor, self.patch)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return self.as_tuple() == other.as_tuple()

        return False

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self) -> str:
        return f"Version ({self})"
