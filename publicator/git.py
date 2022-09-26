"""Git operations"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Mapping, Tuple

from parse import Parser, Result, compile
from semmy import Semver

from publicator import shell


class RemoteParser:
    parser: Parser

    def __init__(self) -> None:
        self.parser = compile("git@{server}:{owner}/{name}.git")

    def parse(self, remote: str) -> Mapping[str, str]:
        result = self.parser.parse(remote)

        if not isinstance(result, Result):
            return {}

        named: Mapping[str, str] = result.named
        return named


@dataclass(frozen=True)
class Repo:
    server: str = ""
    owner: str = ""
    name: str = ""

    @classmethod
    def from_remote(cls) -> Repo:
        parser = RemoteParser()
        remote = shell.run("git remote get-url --push origin").pop()
        values = parser.parse(remote)

        return cls(server=values.get("server", ""), owner=values.get("owner", ""), name=values.get("name", ""))

    @property
    def is_github(self) -> bool:
        return "github.com" in self.server


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


def create_tag(version: Semver, message: str) -> List[str]:
    return shell.run(f'git tag -a {version} -m "{message.strip()}"')


def delete_tag(version: Semver) -> List[str]:
    return shell.run(f"git tag -d {version}")


def push() -> List[str]:
    return shell.run("git push --follow-tags")


def reset() -> List[str]:
    return shell.run("git reset --hard")
