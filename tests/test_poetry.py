from unittest.mock import MagicMock
from publicator import poetry
from semmy import Semver


class TestPoetry:
    def test_poetry_install(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = [
            "Installing dependencies from lock file",
            "No dependencies to install or update",
            "Installing the current project: publicator (1.2.3)",
        ]

        assert poetry.install()

    def test_run_pytest(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["test session starts"]
        assert poetry.run("pytest")

    def test_run_unittest(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Ran 1 test in 0.000s"]
        assert poetry.run("python -m unittest")

    def test_verify_project_health(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["All set!"]
        assert poetry.ok()

    def test_building_package(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Building publicator (1.2.3)"]
        assert poetry.build()

    def test_publishing_the_package(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Publishing publicator (1.2.3)"]
        assert poetry.publish(repository=None)

    def test_version_is_returned(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["1.2.3"]
        assert poetry.version() == Semver(1, 2, 3)
