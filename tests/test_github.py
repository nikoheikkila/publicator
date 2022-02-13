from pytest import fixture, raises
from publicator import github
from semmy import Semver
from publicator.git import Repo


@fixture()
def repo() -> Repo:
    return Repo(server="github.com", owner="nikoheikkila", name="publicator")


@fixture()
def tag() -> Semver:
    return Semver(1, 2, 3)


def test_new_release_url_with_required_variables(repo: Repo, tag: Semver) -> None:
    url = github.new_release_url(repo, tag)
    expected = "https://github.com/nikoheikkila/publicator/releases/new?tag=1.2.3&title=&body=&prerelease=0"

    assert url == expected


def test_new_release_url_with_all_variables(repo: Repo) -> None:
    tag = Semver(0, 1, 0)

    url = github.new_release_url(repo, tag, title=f"Version {tag}", body="# Changelog")

    expected = (
        "https://github.com/nikoheikkila/publicator/releases/new?"
        "tag=0.1.0&title=Version+0.1.0&body=%23+Changelog&prerelease=1"
    )

    assert url == expected


def test_new_release_url_throws_for_non_github_repos(tag: Semver) -> None:
    repo = Repo(server="bitbucket.org", owner="user", name="stuff")

    with raises(github.ReleaseException, match="Current repository is not hosted on github.com"):
        github.new_release_url(
            repo,
            tag,
        )
