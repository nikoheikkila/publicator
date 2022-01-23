from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Tuple

# It ain't perfect but it's an honest day of work.
SEMVER_REGEX = re.compile(r"^\d\.\d\.\d$", re.MULTILINE)


class SemverException(Exception):
    pass


@dataclass(frozen=True)
class Semver:
    major: int = 0
    minor: int = 1
    patch: int = 0

    @classmethod
    def from_string(self, version: str) -> Semver:
        major, minor, patch = map(int, Semver.validate(version).split("."))
        return Semver(major, minor, patch)

    @staticmethod
    def validate(version: str) -> str:
        if not SEMVER_REGEX.match(version):
            raise SemverException(f"Version string {version} is not a valid semantic version")

        return version

    def as_tuple(self) -> Tuple[int, int, int]:
        return (self.major, self.minor, self.patch)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return self.as_tuple() == other.as_tuple()

        return False

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self) -> str:
        return f"Version ({self})"
