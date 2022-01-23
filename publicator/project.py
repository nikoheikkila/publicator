from typing import Any
import toml
from pathlib import Path
from mergedeep import merge

from publicator.semver import Semver

def get_version() -> Semver:
    project = read_project_data()
    version = project['tool']['poetry']['version']

    return Semver.from_string(version)

def bump_version(version: str, filename: str = "pyproject.toml") -> Semver:
    path = Path.cwd() / filename
    project = read_project_data(path.name)

    bump = {
        "tool": {
            "poetry": {
                "version": version
            }
        }
    }

    new_contents = toml.dumps(merge({}, project, bump))
    path.write_text(new_contents)

    return Semver.from_string(version)

def read_project_data(filename: str = "pyproject.toml") -> dict[str, Any]:
    pyproject = Path.cwd() / filename
    return toml.loads(pyproject.read_text())
