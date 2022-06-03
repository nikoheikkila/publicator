from unittest.mock import MagicMock
from hypothesis import given
from hypothesis.strategies import builds, text, just

from publicator import git
from semmy import Semver


def test_get_current_branch(mock_shell: MagicMock) -> None:
    effects = {"git symbolic-ref --short HEAD": ["main"]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    assert git.current_branch() == "main"


def test_get_release_branches() -> None:
    assert git.release_branches() == ("main", "master")


def test_working_directory_is_clean(mock_shell: MagicMock) -> None:
    mock_shell.side_effect = lambda _: []
    assert git.is_working_directory_clean()


def test_working_directory_is_dirty(mock_shell: MagicMock) -> None:
    effects = {"git status --porcelain": ["M poetry.lock", "M pyproject.toml"]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    assert not git.is_working_directory_clean()


def test_stash(mock_shell: MagicMock) -> None:
    effects = {"git stash -u": ["Saved working directory and index state WIP on main"]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    assert git.stash()


def test_pull(mock_shell: MagicMock) -> None:
    effects = {"git pull --rebase": ["Everything up-to-date"]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    assert git.pull()


def test_pop(mock_shell: MagicMock) -> None:
    effects = {"git stash pop": ["Dropped refs"]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    assert git.pop()


def test_add_changes(mock_shell: MagicMock) -> None:
    effects = {"git add pyproject.toml": [""]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    assert git.add()


def test_commit_changes(mock_shell: MagicMock) -> None:
    expected_output = ["1 file changed"]
    effects = {'git commit -m "release: 1.2.3"': expected_output}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    assert git.commit(message="release: 1.2.3") == expected_output


def test_creating_tag(mock_shell: MagicMock) -> None:
    effects = {'git tag -a 1.2.3 -m "Version 1.2.3"': [""]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    assert git.create_tag(version=Semver(1, 2, 3), message="Version 1.2.3")


def test_pushing_changes(mock_shell: MagicMock) -> None:
    effects = {"git push --follow-tags": ["Everything up-to-date"]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    assert git.push()


def test_extract_repo_from_invalid_remote(mock_shell: MagicMock) -> None:
    effects = {"git remote get-url --push origin": ["no remote"]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    repo = git.Repo.from_remote()

    assert repo == git.Repo()


def test_remote_parser_initializes_correctly() -> None:
    remote = git.RemoteParser()

    assert remote.parser._expression == r"git@(?P<server>.+?):(?P<owner>.+?)/(?P<name>.+?)\.git"


def test_extract_repo_from_remote(mock_shell: MagicMock) -> None:
    effects = {"git remote get-url --push origin": ["git@github.com:nikoheikkila/publicator.git"]}
    mock_shell.side_effect = lambda cmd: effects.get(cmd, [])

    repo = git.Repo.from_remote()

    assert repo.server == "github.com"
    assert repo.owner == "nikoheikkila"
    assert repo.name == "publicator"


def test_remote_parser_with_invalid_git_remote() -> None:
    remote = git.RemoteParser()
    result = remote.parse("nonsense")

    assert not result.keys()


@given(builds(git.Repo, server=just("github.com"), owner=text(), name=text()))
def test_repo_is_from_github(repo: git.Repo) -> None:
    assert repo.is_github


@given(builds(git.Repo, server=just("gitlab.com"), owner=text(), name=text()))
def test_repo_is_not_from_github(repo: git.Repo) -> None:
    assert not repo.is_github
