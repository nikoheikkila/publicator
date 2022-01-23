from pytest import raises
from pytest_mock import MockerFixture
from publicator import project
from publicator.semver import Semver, SemverException

def test_get_version_returns_semantic_version(mocker: MockerFixture):
    mock_toml = """
    [tool.poetry]
    version = "1.2.3"
    """
    mocker.patch("pathlib.Path.read_text", lambda path: mock_toml)

    assert project.get_version() == Semver(1, 2, 3)

def test_get_version_fails_for_missing_version(mocker: MockerFixture):
    mock_toml = "[tool.poetry]"
    mocker.patch("pathlib.Path.read_text", lambda path: mock_toml)

    with raises(KeyError):
        project.get_version()

def test_get_version_fails_for_invalid_version(mocker: MockerFixture):
    mock_toml = """
    [tool.poetry]
    version = "N/A"
    """
    mocker.patch("pathlib.Path.read_text", lambda path: mock_toml)

    with raises(SemverException, match="Version string N/A is not a valid semantic version"):
        project.get_version()

def test_bump_version_returns_bumped_version(mocker: MockerFixture):
    mocker.patch("pathlib.Path.write_text", autospec=True)

    assert project.bump_version("1.2.3") == Semver(1, 2, 3)
