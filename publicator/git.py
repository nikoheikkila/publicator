"""Git operations"""

from publicator import shell

def current_branch() -> str:
    return shell.run("git symbolic-ref --short HEAD").pop()

def release_branches() -> tuple[str, str]:
    return ("main", "master")