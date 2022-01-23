from typing import Tuple
from unittest.mock import MagicMock
from pytest import fixture
from pytest_mock import MockerFixture
from pathlib import Path
from publicator import shell

@fixture()
def mock_shell(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(shell, 'run', autospec=True)

@fixture()
def mock_path(mocker: MockerFixture) -> Tuple[MagicMock]:
    return (
        mocker.path.object(Path, 'read_text', autospec=True),
        mocker.path.object(Path, 'write_text', autospec=True),
    )
