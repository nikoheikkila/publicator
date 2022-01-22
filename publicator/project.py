import toml
from pathlib import Path

def get_version() -> str:
    pyproject = Path.cwd() / "pyproject.toml"

    with pyproject.open(mode="r") as f:
        contents = toml.load(f)

    return contents['tool']['poetry']['version']
