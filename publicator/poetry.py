from typing import List, Optional
from publicator import shell
from publicator.semver import Semver


def install() -> List[str]:
    return shell.run("poetry install --remove-untracked")


def run(command: str) -> List[str]:
    return shell.run(f"poetry run {command.strip()}")


def ok() -> bool:
    result = shell.run("poetry check").pop()
    return "All set" in result


def build() -> List[str]:
    return shell.run("poetry build")


def publish(repository: Optional[str] = None) -> List[str]:
    command = "poetry publish"

    if repository:
        command += f" --repository {repository}"

    return shell.run(command)


def version() -> Semver:
    result = shell.run("poetry version --short").pop()
    return Semver.from_string(result)


def bump(increment: str) -> Semver:
    shell.run(f"poetry version {increment}")
    return version()
