"""Git operations"""

from publicator import shell

def current_branch() -> str:
    return shell.run("git symbolic-ref --short HEAD").pop()

def release_branches() -> tuple[str, str]:
    return ("main", "master")

def status() -> list[str]:
    return shell.run("git status --porcelain")

def is_working_directory_clean() -> bool:
    return len(status()) == 0

def stash() -> list[str]:
    return shell.run("git stash -u")

def pull() -> list[str]:
    return shell.run("git pull --rebase")

def pop() -> list[str]:
    return shell.run("git stash pop")

def add() -> list[str]:
    return shell.run("git add pyproject.toml")

def commit(message: str) -> list[str]:
    return shell.run(f'git commit -m "{message.strip()}"')

def create_tag(version: str, message: str) -> list[str]:
    return shell.run(f'git tag -a {version.strip()} -m "{message.strip()}"')

def push() -> list[str]:
    return shell.run("git push --follow-tags")
