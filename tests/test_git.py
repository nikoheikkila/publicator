from publicator import git


def test_get_current_branch():
    assert git.current_branch() == "main"

def test_get_release_branches():
    assert git.release_branches() == ("main", "master")