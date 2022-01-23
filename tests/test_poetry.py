from unittest.mock import MagicMock
from publicator import poetry
from publicator.semver import Semver


def test_poetry_install(mock_shell: MagicMock):
    mock_shell.return_value = [
        "Installing dependencies from lock file",
        "No dependencies to install or update",
        "Installing the current project: publicator (1.2.3)",
    ]

    assert poetry.install()


def test_run_pytest(mock_shell: MagicMock):
    mock_shell.return_value = ["test session starts"]
    assert poetry.run_tests()


def test_run_unittest(mock_shell: MagicMock):
    mock_shell.return_value = ["Ran 1 test in 0.000s"]
    assert poetry.run_tests(command="python -m unittest")


def test_verify_project_health(mock_shell: MagicMock):
    mock_shell.return_value = ["All set!"]
    assert poetry.ok()


def test_building_package(mock_shell: MagicMock):
    mock_shell.return_value = ["Building publicator (1.2.3)"]
    assert poetry.build()


def test_publishing_the_package(mock_shell: MagicMock):
    mock_shell.return_value = ["Publishing publicator (1.2.3)"]
    assert poetry.publish(repository=None, dry_run=True)


def test_version_is_returned(mock_shell: MagicMock):
    mock_shell.return_value = ["1.2.3"]
    assert poetry.version() == Semver(1, 2, 3)
