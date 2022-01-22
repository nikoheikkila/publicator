from os import major
from unittest.mock import MagicMock
from publicator import project
from publicator.semver import Semver

def test_version_reading(mock_toml: MagicMock):
    version = "0.1.0"
    mock_toml.return_value = {
        "tool": {
            "poetry": {
                "name": "publicator",
                "version": version
            }
        }
    }

    assert project.get_version() == Semver(major=0, minor=1, patch=0)

# def test_bump_version():
#     version.bump("1.2.3")
#     version.get() == "1.2.3"