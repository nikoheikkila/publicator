import toml
from pathlib import Path

from publicator.semver import Semver

def get_version() -> Semver:
    pyproject = Path.cwd() / "pyproject.toml"

    with pyproject.open(mode="r") as f:
        contents = toml.load(f)

    version = contents['tool']['poetry']['version']
    return Semver.from_string(version)
