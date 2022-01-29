from unittest.mock import MagicMock

from publicator import git
from publicator.semver import Semver


def test_get_current_branch(mock_shell: MagicMock) -> None:
    mock_shell.return_value = ["main"]
    assert git.current_branch() == "main"


def test_get_release_branches() -> None:
    assert git.release_branches() == ("main", "master")


def test_working_directory_is_clean(mock_shell: MagicMock) -> None:
    mock_shell.return_value = []
    assert git.is_working_directory_clean()


def test_working_directory_is_dirty(mock_shell: MagicMock) -> None:
    mock_shell.return_value = ["M poetry.lock", "M pyproject.toml"]
    assert not git.is_working_directory_clean()


def test_stash(mock_shell: MagicMock) -> None:
    mock_shell.return_value = ["Saved working directory and index state WIP on main"]
    assert git.stash()


def test_pull(mock_shell: MagicMock) -> None:
    mock_shell.return_value = ["Everything up-to-date"]
    assert git.pull()


def test_pop(mock_shell: MagicMock) -> None:
    mock_shell.return_value = ["Dropped refs"]
    assert git.pop()


def test_add_changes(mock_shell: MagicMock) -> None:
    mock_shell.return_value = [""]
    assert git.add()


def test_commit_changes(mock_shell: MagicMock) -> None:
    expected_output = ["1 file changed"]
    mock_shell.return_value = expected_output
    assert git.commit(message="release: 1.2.3") == expected_output


def test_creating_tag(mock_shell: MagicMock) -> None:
    mock_shell.return_value = [""]
    assert git.create_tag(version=Semver(1, 2, 3), message="Version 1.2.3")


def test_pushing_changes(mock_shell: MagicMock) -> None:
    mock_shell.return_value = ["Everything up-to-date"]
    assert git.push()


def test_extract_repo_from_remote(mock_shell: MagicMock) -> None:
    mock_shell.return_value = ["git@github.com:nikoheikkila/publicator.git"]

    repo = git.Repo.from_remote()

    assert repo.server == "github.com"
    assert repo.owner == "nikoheikkila"
    assert repo.name == "publicator"


def test_extract_repo_from_invalid_remote(mock_shell: MagicMock) -> None:
    mock_shell.return_value = ["no remote"]

    repo = git.Repo.from_remote()

    assert repo == git.Repo()


def test_repo_is_from_github() -> None:
    repo = git.Repo(server="github.com")
    assert repo.is_github


def test_repo_is_not_from_github() -> None:
    repo = git.Repo(server="gitlab.com")
    assert not repo.is_github
