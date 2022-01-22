from typing import Any
import toml
from pathlib import Path
from mergedeep import merge

from publicator.semver import Semver

def get_version() -> Semver:
    pyproject = Path.cwd() / "pyproject.toml"
    contents: dict[str, Any] = toml.loads(pyproject.read_text())
    version = contents['tool']['poetry']['version']

    return Semver.from_string(version)

def bump_version(version: str) -> Semver:
    pyproject = Path.cwd() / "pyproject.toml"

    contents: dict[str, Any] = toml.loads(pyproject.read_text())
    bump = {
        "tool": {
            "poetry": {
                "version": version
            }
        }
    }

    new_contents = merge({}, contents, bump)

    pyproject.write_text(toml.dumps(new_contents))

    return Semver.from_string(version)
