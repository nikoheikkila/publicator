from unittest.mock import MagicMock

from assertpy import assert_that as verify
from hypothesis import given
from hypothesis.strategies import builds, just, text
from publicator import git
from semmy import Semver


class TestGit:
    def test_get_current_branch(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["main"]

        current_branch = git.current_branch()

        verify(current_branch).is_equal_to("main")
        verify(mock_shell.assert_called_once_with("git symbolic-ref --short HEAD"))

    def test_get_release_branches(self) -> None:
        branches = git.release_branches()

        verify(branches).is_length(2).contains("main", "master")

    def test_working_directory_is_clean(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = []

        verify(git.is_working_directory_clean()).is_true()
        verify(mock_shell.assert_called_once_with("git status --porcelain"))

    def test_working_directory_is_dirty(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["M poetry.lock", "M pyproject.toml"]

        verify(git.is_working_directory_clean()).is_false()
        verify(mock_shell.assert_called_once_with("git status --porcelain"))

    def test_stash(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Saved working directory and index state WIP on main"]

        verify(git.stash()).is_not_empty()
        verify(mock_shell.assert_called_once_with("git stash -u"))

    def test_pull(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Everything up-to-date"]

        verify(git.pull()).is_not_empty()
        verify(mock_shell.assert_called_once_with("git pull --rebase"))

    def test_pop(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Dropped refs"]

        verify(git.pop()).is_not_empty()
        verify(mock_shell.assert_called_once_with("git stash pop"))

    def test_add_changes(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = [""]

        verify(git.add()).is_not_empty()
        verify(mock_shell.assert_called_once_with("git add pyproject.toml"))

    def test_commit_changes(self, mock_shell: MagicMock) -> None:
        expected_output = ["1 file changed"]
        mock_shell.return_value = expected_output

        verify(git.commit(message="release: 1.2.3")).is_equal_to(expected_output)
        verify(mock_shell.assert_called_once_with('git commit -m "release: 1.2.3"'))

    def test_creating_tag(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = [""]

        verify(git.create_tag(version=Semver(1, 2, 3), message="Version 1.2.3")).is_not_empty()
        verify(mock_shell.assert_called_once_with('git tag -a 1.2.3 -m "Version 1.2.3"'))

    def test_deleting_tag(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Deleted tag '1.2.3'"]

        verify(git.delete_tag(version=Semver(1, 2, 3))).is_not_empty()
        verify(mock_shell.assert_called_once_with("git tag -d 1.2.3"))

    def test_pushing_changes(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["Everything up-to-date"]

        verify(git.push()).is_not_empty()
        verify(mock_shell.assert_called_once_with("git push --follow-tags"))

    def test_reset(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["HEAD is now at abc1234 chore: initial commit"]

        verify(git.reset()).is_not_empty()
        verify(mock_shell.assert_called_once_with("git reset --hard"))

    def test_extract_repo_from_invalid_remote(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["no remote"]
        expected_repository = git.Repo()

        actual_repository = git.Repo.from_remote()

        verify(actual_repository).is_equal_to(expected_repository)
        verify(mock_shell.assert_called_once_with("git remote get-url --push origin"))

    def test_remote_parser_initializes_correctly(self) -> None:
        remote = git.RemoteParser()

        verify(remote.parser._expression).is_equal_to(r"git@(?P<server>.+?):(?P<owner>.+?)/(?P<name>.+?)\.git")

    def test_extract_repo_from_remote(self, mock_shell: MagicMock) -> None:
        mock_shell.return_value = ["git@github.com:nikoheikkila/publicator.git"]

        repo = git.Repo.from_remote()

        verify(repo).has_server("github.com").has_owner("nikoheikkila").has_name("publicator")
        verify(mock_shell.assert_called_once_with("git remote get-url --push origin"))

    def test_remote_parser_with_invalid_git_remote(self) -> None:
        remote = git.RemoteParser()

        result = remote.parse("nonsense").keys()

        verify(result).is_empty()

    @given(builds(git.Repo, server=just("github.com"), owner=text(), name=text()))
    def test_repo_is_from_github(self, repo: git.Repo) -> None:
        verify(repo.is_github).is_true()

    @given(builds(git.Repo, server=text(), owner=text(), name=text()))
    def test_repo_is_not_from_github(self, repo: git.Repo) -> None:
        verify(repo.is_github).is_false()
