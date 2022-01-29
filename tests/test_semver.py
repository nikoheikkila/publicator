from publicator.semver import Semver


def test_semver_prerelease() -> None:
    assert Semver.from_string("0.0.1-alpha.0") == Semver(0, 0, 1, pre_release="alpha.0")


def test_semver_patch() -> None:
    assert Semver.from_string("0.0.1") == Semver(0, 0, 1)


def test_semver_minor() -> None:
    assert Semver.from_string("0.1.0") == Semver(0, 1, 0)


def test_semver_major() -> None:
    assert Semver.from_string("1.0.0") == Semver(1, 0, 0)


def test_semver_build_metadata() -> None:
    assert Semver.from_string("1.0.0+ABC") == Semver(1, 0, 0, build="ABC")
