from unittest.mock import MagicMock
from pytest import fixture
from pytest_mock import MockerFixture
import toml

from publicator import shell

@fixture()
def mock_shell(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(shell, 'run', autospec=True)

@fixture()
def mock_toml(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(toml, 'load', autospec=True)