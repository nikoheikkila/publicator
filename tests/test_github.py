from publicator import github
from publicator.git import Repo
from pytest import fixture, raises
from semmy import Semver
from assertpy import assert_that as verify


class TestGitHub:
    @fixture()
    def repo(self) -> Repo:
        return Repo(server="github.com", owner="nikoheikkila", name="publicator")

    @fixture()
    def tag(self) -> Semver:
        return Semver(1, 2, 3)

    def test_new_release_url_with_required_variables(self, repo: Repo, tag: Semver) -> None:
        url = github.new_release_url(repo, tag)
        expected = "https://github.com/nikoheikkila/publicator/releases/new?tag=1.2.3&title=&body=&prerelease=0"

        verify(url).is_equal_to(expected)

    def test_new_release_url_with_all_variables(self, repo: Repo) -> None:
        tag = Semver(0, 1, 0)
        expected = (
            "https://github.com/nikoheikkila/publicator/releases/new?"
            "tag=0.1.0&title=Version+0.1.0&body=%23+Changelog&prerelease=1"
        )

        url = github.new_release_url(repo, tag, title=f"Version {tag}", body="# Changelog")

        verify(url).is_equal_to(expected)

    def test_new_release_url_throws_for_non_github_repos(self, tag: Semver) -> None:
        repo = Repo(server="bitbucket.org", owner="user", name="stuff")

        with raises(AssertionError, match="Current repository is not hosted on github.com"):
            github.new_release_url(
                repo,
                tag,
            )
