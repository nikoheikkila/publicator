from unittest.mock import MagicMock
from publicator import project

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

    assert project.get_version() == version

# def test_bump_version():
#     version.bump("1.2.3")
#     version.get() == "1.2.3"