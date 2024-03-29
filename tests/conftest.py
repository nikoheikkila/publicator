from unittest.mock import MagicMock
from pytest import fixture
from pytest_mock import MockerFixture
from pathlib import Path

from publicator import shell


@fixture()
def mock_shell(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(shell, "run", autospec=True)


@fixture()
def mock_read_text(mocker: MockerFixture) -> MagicMock:
    mocker.patch.object(Path, "is_file").return_value = True
    mock = mocker.patch.object(Path, "read_text", autospec=True)

    return mock
