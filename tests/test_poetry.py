from unittest.mock import MagicMock
from publicator import poetry
from semmy import Semver
from assertpy import assert_that as verify


class TestPoetry:
    def test_poetry_install(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = [
            "Installing dependencies from lock file",
            "No dependencies to install or update",
            "Installing the current project: publicator (1.2.3)",
        ]

        verify(poetry.install()).is_not_empty()
        verify(mock_shell.assert_called_once_with("poetry install --remove-untracked"))

    def test_run_pytest(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["test session starts"]

        verify(poetry.run("pytest")).is_not_empty()
        verify(mock_shell.assert_called_once_with("poetry run pytest"))

    def test_run_unittest(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Ran 1 test in 0.000s"]

        verify(poetry.run("python -m unittest")).is_not_empty()
        verify(mock_shell.assert_called_once_with("poetry run python -m unittest"))

    def test_verify_project_health(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["All set!"]

        verify(poetry.ok()).is_true()
        verify(mock_shell.assert_called_once_with("poetry check"))

    def test_building_package(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Building publicator (1.2.3)"]

        verify(poetry.build()).is_not_empty()
        verify(mock_shell.assert_called_once_with("poetry build"))

    def test_publishing_the_package(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Publishing publicator (1.2.3)"]

        verify(poetry.publish(repository=None)).is_not_empty()
        verify(mock_shell.assert_called_once_with("poetry publish"))

    def test_version_is_returned(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["1.2.3"]

        verify(poetry.version()).is_equal_to(Semver(1, 2, 3))
        verify(mock_shell.assert_called_once_with("poetry version --short"))
