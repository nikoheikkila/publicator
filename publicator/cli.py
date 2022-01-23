import os
from typing import Optional
import typer

from publicator import git, poetry
from publicator.semver import Semver

preview = os.environ.get("PUBLICATOR_PREVIEW")

app = typer.Typer(name="publicator")


@app.command()
def cli(
    version: str = typer.Argument(
        ...,
        metavar="version",
        help="can be a valid semver or one of: patch, minor, major, prepatch, preminor, premajor, prerelease",
    ),
    repository: Optional[str] = typer.Option(
        default=None, metavar="name", help="Custom repository for publishing (must be specified in pyproject.toml)"
    ),
    any_branch: bool = typer.Option(default=False, help="Allow publishing from any branch"),
    skip_cleaning: bool = typer.Option(default=False, help="Skip repository clean up"),
    yolo: bool = typer.Option(default=False, help="Skip reinstall and test steps"),
    skip_tag: bool = typer.Option(default=False, help="Skip creating a new tag"),
    skip_publish: bool = typer.Option(default=False, help="Skip publishing the package to the registry"),
    skip_push: bool = typer.Option(default=False, help="Skip pushing commits and tags to Git"),
) -> None:
    if not any_branch:
        verify_branch()

    if not skip_cleaning:
        clean_up()

    if not yolo:
        install_dependencies()
        run_tests()

    new_version = bump_version(version)
    commit_changes(new_version)

    if not skip_tag:
        create_tag(new_version)

    build_package()

    if not skip_publish:
        publish_package(repository, skip_publish)

    if not skip_push:
        push()

    success("Published the new package version. Cheers!")


def info(message: str) -> None:
    typer.secho(f"📢 {message}", fg=typer.colors.BRIGHT_BLUE)


def success(message: str) -> None:
    typer.secho(f"🎉 {message}", fg=typer.colors.BRIGHT_GREEN, bold=True)


def fatal(message: str, exit_code: int = 1) -> None:
    typer.secho(f"❌ {message}", fg=typer.colors.BRIGHT_RED, bold=True)
    raise typer.Exit(code=exit_code)


def push() -> None:
    info("Pushing changes to Git")
    if not preview:
        git.push()


def publish_package(repository: Optional[str], skip_publish: bool) -> None:
    info("Publishing the package to repository")
    if not preview:
        poetry.publish(repository, dry_run=skip_publish)


def build_package() -> None:
    info("Building the package")
    if not preview:
        poetry.build()


def create_tag(version: Semver) -> None:
    info(f"Creating a new tag {version} from HEAD")
    if not preview:
        git.create_tag(version, message=f"Version {version}")


def commit_changes(semver: Semver) -> None:
    info("Committing changes")
    if not preview:
        poetry.ok()
        git.add()
        git.commit(f"release: {semver}")


def bump_version(version: str) -> Semver:
    current_version = poetry.version()

    if preview:
        return current_version

    next_version = poetry.bump(version)
    info(f"Bumped version from {current_version} to {next_version}")

    return next_version


def run_tests() -> None:
    info("Running tests")
    if not preview:
        poetry.run_tests()


def install_dependencies() -> None:
    info("Reinstalling dependencies")
    if not preview:
        poetry.install()


def clean_up() -> None:
    if git.is_working_directory_clean():
        return

    if not preview:
        info("Resetting working directory to a clean state")
        git.stash()
        git.pull()
        git.pop()


def verify_branch() -> None:
    current_branch = git.current_branch()
    release_branches = git.release_branches()

    if current_branch not in release_branches:
        fatal(f"Current checked out branch {current_branch} is not a release branch {release_branches}")
