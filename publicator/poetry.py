from typing import List, Optional
from publicator import shell


def install() -> List[str]:
    return shell.run("poetry install --remove-untracked")


def run_tests(command: str = "pytest") -> List[str]:
    return shell.run(f"poetry run {command.strip()}")


def ok() -> bool:
    result = shell.run("poetry check").pop()
    return "All set" in result


def build() -> List[str]:
    return shell.run("poetry build")


def publish(repository: Optional[str] = None, dry_run: bool = False) -> List[str]:
    command = "poetry publish"

    if repository:
        command += f" --repository {repository}"
    if dry_run:
        command += " --dry-run"

    return shell.run(command)
