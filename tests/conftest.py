from unittest.mock import MagicMock
from pytest import fixture
from pytest_mock import MockerFixture
from pathlib import Path
from publicator import shell


@fixture()
def mock_shell(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(shell, "run")


@fixture()
def mock_read_text(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(Path, "read_text")
