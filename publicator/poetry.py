from publicator import shell


def install() -> list[str]:
    return shell.run("poetry install --remove-untracked")

def run_tests(command: str = "pytest") -> list[str]:
    return shell.run(f"poetry run {command.strip()}")