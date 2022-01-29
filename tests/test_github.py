from pytest import fixture
from publicator import github
from publicator.semver import Semver
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


def test_new_release_url_with_all_variables(repo: Repo, tag: Semver) -> None:
    url = github.new_release_url(
        repo,
        tag,
        title=f"Version {tag}",
        body="# Changelog",
        pre_release=True,
    )

    expected = (
        "https://github.com/nikoheikkila/publicator/releases/new?"
        "tag=1.2.3&title=Version+1.2.3&body=%23+Changelog&prerelease=1"
    )

    assert url == expected
