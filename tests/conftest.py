from unittest.mock import MagicMock
from pytest import fixture
from pytest_mock import MockerFixture
import toml
from pathlib import Path
from publicator import shell

@fixture()
def mock_shell(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(shell, 'run', autospec=True)

@fixture()
def mock_toml(mocker: MockerFixture) -> tuple[MagicMock]:
    return (
        mocker.patch.object(toml, 'loads', autospec=True),
        mocker.patch.object(toml, 'dumps', autospec=True),
    )

@fixture()
def mock_path(mocker: MockerFixture) -> tuple[MagicMock]:
    return (
        mocker.path.object(Path, 'read_text', autospec=True),
        mocker.path.object(Path, 'write_text', autospec=True),
    )
