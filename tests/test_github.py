from publicator import github
from publicator.semver import Semver


def test_new_release_url_with_required_variables() -> None:
    url = github.new_release_url(owner="nikoheikkila", repository="publicator", tag=Semver(1, 2, 3))
    expected = "https://github.com/nikoheikkila/publicator/releases/new?tag=1.2.3&title=&body=&prerelease=0"

    assert url == expected


def test_new_release_url_with_all_variables() -> None:
    url = github.new_release_url(
        owner="nikoheikkila",
        repository="publicator",
        tag=Semver(1, 2, 3),
        title="Version 1.2.3",
        body="# Changelog",
        pre_release=True,
    )

    expected = (
        "https://github.com/nikoheikkila/publicator/releases/new?"
        "tag=1.2.3&title=Version+1.2.3&body=%23+Changelog&prerelease=1"
    )

    assert url == expected
