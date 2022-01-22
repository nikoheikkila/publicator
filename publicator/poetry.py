from typing import Optional
from publicator import shell


def install() -> list[str]:
    return shell.run("poetry install --remove-untracked")

def run_tests(command: str = "pytest") -> list[str]:
    return shell.run(f"poetry run {command.strip()}")

def ok() -> bool:
    result = shell.run("poetry check").pop()
    return "All set" in result

def build() -> list[str]:
    return shell.run("poetry build")

def publish(repository: Optional[str] = None, dry_run: bool = False) -> list[str]:
    command = "poetry publish"

    if repository:
        command += f" --repository {repository}"
    if dry_run:
        command += f" --dry-run"

    return shell.run(command)
