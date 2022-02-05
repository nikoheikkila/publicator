from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Tuple

# See: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
SEMVER_REGEX = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))"
    r"?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
    re.MULTILINE,
)


class SemverException(Exception):
    pass


@dataclass(frozen=True)  # pragma: no mutate
class Semver:
    major: int = 0
    minor: int = 1
    patch: int = 0
    pre_release: str = ""
    build: str = ""

    @property
    def is_pre_release(self) -> bool:
        if self.pre_release:
            return True

        return self.major == 0

    @classmethod
    def from_string(cls, version: str) -> Semver:
        if not SEMVER_REGEX.fullmatch(version):
            raise SemverException(f"Version string {version} is not a valid semantic version")

        major, minor, patch, pre_release, build = SEMVER_REGEX.findall(version).pop()

        return Semver(int(major), int(minor), int(patch), pre_release, build)

    def as_tuple(self) -> Tuple[int, int, int]:
        return (self.major, self.minor, self.patch)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return str(self) == str(other)

        return False

    def __str__(self) -> str:
        result = f"{self.major}.{self.minor}.{self.patch}"

        if self.pre_release:
            result += f"-{self.pre_release}"
        if self.build:
            result += f"+{self.build}"

        return result

    def __repr__(self) -> str:
        return f"Version ({self})"
