"""Git operations"""
from typing import List, Tuple

from publicator import shell

def current_branch() -> str:
    return shell.run("git symbolic-ref --short HEAD").pop()

def release_branches() -> Tuple[str, str]:
    return ("main", "master")

def status() -> List[str]:
    return shell.run("git status --porcelain")

def is_working_directory_clean() -> bool:
    return len(status()) == 0

def stash() -> List[str]:
    return shell.run("git stash -u")

def pull() -> List[str]:
    return shell.run("git pull --rebase")

def pop() -> List[str]:
    return shell.run("git stash pop")

def add() -> List[str]:
    return shell.run("git add pyproject.toml")

def commit(message: str) -> List[str]:
    return shell.run(f'git commit -m "{message.strip()}"')

def create_tag(version: str, message: str) -> List[str]:
    return shell.run(f'git tag -a {version.strip()} -m "{message.strip()}"')

def push() -> List[str]:
    return shell.run("git push --follow-tags")
