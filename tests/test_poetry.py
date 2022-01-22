from unittest.mock import MagicMock
from publicator import poetry

def test_poetry_install(mock_shell: MagicMock):
    mock_shell.return_value = [
        "Installing dependencies from lock file",
        "No dependencies to install or update",
        "Installing the current project: publicator (1.2.3)"
    ]

    assert poetry.install()

def test_run_pytest(mock_shell: MagicMock):
    mock_shell.return_value = ["test session starts"]
    assert poetry.run_tests()

def test_run_unittest(mock_shell: MagicMock):
    mock_shell.return_value = ["Ran 1 test in 0.000s"]
    assert poetry.run_tests(command="python -m unittest")
