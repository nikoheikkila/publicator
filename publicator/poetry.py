from publicator import shell


def install() -> list[str]:
    return shell.run("poetry install --remove-untracked")

def run_tests(command: str = "pytest") -> list[str]:
    return shell.run(f"poetry run {command.strip()}")

def ok() -> bool:
    result = shell.run("poetry check").pop()
    return "All set" in result