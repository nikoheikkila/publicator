from publicator import shell


def install() -> list[str]:
    return shell.run("poetry install --remove-untracked")