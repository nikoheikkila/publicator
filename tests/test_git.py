from unittest.mock import MagicMock

from publicator import git

def test_get_current_branch(mock_shell: MagicMock):
    mock_shell.return_value = ["main"]
    assert git.current_branch() == "main"

def test_get_release_branches():
    assert git.release_branches() == ("main", "master")

def test_working_directory_is_clean(mock_shell: MagicMock):
    mock_shell.return_value = []
    assert git.is_working_directory_clean()

def test_working_directory_is_dirty(mock_shell: MagicMock):
    mock_shell.return_value = ["M poetry.lock", "M pyproject.toml"]
    assert not git.is_working_directory_clean()

def test_stash(mock_shell: MagicMock):
    mock_shell.return_value = ["Saved working directory and index state WIP on main"]
    assert git.stash()

def test_pull(mock_shell: MagicMock):
    mock_shell.return_value = ["Already up-to-date"]
    assert git.pull()

def test_pop(mock_shell: MagicMock):
    mock_shell.return_value = ["Dropped refs"]
    assert git.pop()
