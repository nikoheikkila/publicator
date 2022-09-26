import os
from subprocess import CalledProcessError
from typing import NoReturn, Optional

import typer
from rich import print
from semmy import Semver

import publicator
from publicator import config, git, github, poetry

preview = os.environ.get("PUBLICATOR_PREVIEW")
configuration = config.factory()
app = typer.Typer(name=publicator.name)


def version_callback(value: bool) -> None:
    if not value:
        return

    print(f"[bold blue]:unicorn_face: {publicator.version()}[/bold blue]")
    raise typer.Exit()


@app.command()
def cli(
    bump: str = typer.Argument(
        ...,
        metavar="version",
        help="can be a valid semver or one of: patch, minor, major, prepatch, preminor, premajor, prerelease",
    ),
    version: Optional[bool] = typer.Option(None, "--version", "-V", callback=version_callback, is_eager=True),
    repository: Optional[str] = typer.Option(
        default=configuration.get("repository"),
        metavar="name",
        help="Custom repository for publishing (must be specified in pyproject.toml)",
    ),
    any_branch: bool = typer.Option(
        default=configuration.get("any-branch", False), help="Allow publishing from any branch"
    ),
    clean: bool = typer.Option(
        default=configuration.get("clean", True), help="Ensure you're working with the latest changes"
    ),
    tag: bool = typer.Option(default=configuration.get("tag", True), help="Create a new tag for Git"),
    publish: bool = typer.Option(
        default=configuration.get("publish", True), help="Publish the package to the registry"
    ),
    push: bool = typer.Option(default=configuration.get("push", True), help="Push commits and tags to Git"),
    test_script: str = typer.Option(
        default=configuration.get("test-script", "pytest -x --assert=plain"),
        help="Name of the test script to run under the current virtual environment",
    ),
    template: str = typer.Option(
        default=configuration.get("template", "release: %s"),
        help="Commit message template (`%s` will be replaced with the new version tag)",
    ),
    release_draft: bool = typer.Option(
        default=configuration.get("release-draft", True),
        help="Opens a pre-filled GitHub release page with browser if the current project is hosted on GitHub",
    ),
) -> None:
    """
    Handles publishing a new Python package via Poetry safely and conveniently.
    """

    if not any_branch:
        verify_branch()

    if clean:
        clean_up()
        install_dependencies()

    if test_script:
        run_tests(test_script)

    new_version = bump_version(bump)
    commit_changes(new_version, template)

    if tag:
        create_tag(new_version)

    if publish:
        build_package()
        publish_package(repository, new_version)

    if push:
        push_changes()

    if release_draft:
        draft_new_release(new_version)

    success("Published the new package version. Cheers!")


def info(message: str) -> None:
    print(f"[blue]:megaphone: {message}[/blue]")


def success(message: str) -> None:
    print(f"[bold green]:party_popper: {message}[/bold green]")


def warn(message: str) -> None:
    print(f"[yellow]:heavy_exclamation_mark: {message}[/yellow]")


def error(message: str) -> None:
    print(f"[red]:cross_mark: {message}[/red]")


def fatal(message: str, exit_code: int = 1) -> NoReturn:
    print(f"[bold red]:cross_mark: {message}[/bold red]")
    raise typer.Exit(code=exit_code)


def draft_new_release(tag: Semver) -> None:
    info("Opening GitHub release draft in browser...")

    if preview:
        return

    repo = git.Repo.from_remote()

    try:
        url = github.new_release_url(repo, tag, title=f"Version {tag}", body="Write here")
        typer.launch(url)
    except AssertionError as error:
        warn(f"Skipping release draft. Reason: {error}")


def push_changes() -> None:
    info("Pushing changes to Git...")

    if preview:
        return

    try:
        git.push()
    except CalledProcessError as e:
        error(e.stderr)
        fatal("Failed to push changes to Git!", exit_code=e.returncode)


def publish_package(repository: Optional[str], version: Semver) -> None:
    info("Publishing the package to repository...")

    if preview:
        return

    try:
        poetry.publish(repository)
    except CalledProcessError as e:
        git.delete_tag(version)
        git.reset()
        error(e.stderr)
        fatal("Failed to publish the package! Repository state has been reset.", exit_code=e.returncode)


def build_package() -> None:
    info("Building the package...")

    if preview:
        return

    try:
        poetry.build()
    except CalledProcessError as e:
        error(e.stderr)
        fatal("Failed to build the package!", exit_code=e.returncode)


def create_tag(version: Semver) -> None:
    info(f"Creating a new tag {version} from HEAD...")

    if preview:
        return

    try:
        git.create_tag(version, message=f"Version {version}")
    except CalledProcessError as e:
        error(e.stderr)
        fatal("Failed to create a new tag!", exit_code=e.returncode)


def commit_changes(semver: Semver, template: str) -> None:
    message = template % (semver)
    info(f'Committing changes with message: "{message}"')

    if preview:
        return

    try:
        poetry.ok()
        git.add()
        git.commit(message)
    except CalledProcessError as e:
        error(e.stderr)
        fatal("Failed to commit changes!", exit_code=e.returncode)


def bump_version(version: str) -> Semver:
    current_version = poetry.version()

    if preview:
        return current_version

    try:
        next_version = poetry.bump(version)
    except CalledProcessError as e:
        error(e.stderr)
        fatal("Failed to bump the version!", exit_code=e.returncode)

    info(f"Bumped version from {current_version} to {next_version}")

    return next_version


def run_tests(script: str) -> None:
    info(f"Running tests with '{script}' ...")

    if preview:
        return

    try:
        poetry.run(script)
    except CalledProcessError as e:
        error(e.stderr)
        fatal("The test runner reported an error!", exit_code=e.returncode)


def install_dependencies() -> None:
    info("Reinstalling project dependencies from pyproject.toml...")

    if preview:
        return

    try:
        poetry.install()
    except CalledProcessError as e:
        error(e.stderr)
        fatal("Failed reinstalling the project dependencies!", exit_code=e.returncode)


def clean_up() -> None:
    if preview or git.is_working_directory_clean():
        return

    info("Resetting working directory to a clean state...")

    try:
        git.stash()
        git.pull()
        git.pop()
    except CalledProcessError as e:
        error(e.stderr)
        fatal("Failed to reset the working directory to a clean state!", exit_code=e.returncode)


def verify_branch() -> None:
    current_branch = git.current_branch()
    release_branches = git.release_branches()

    if current_branch not in release_branches:
        fatal(f"Current checked out branch {current_branch} is not one of allowed release branches: {release_branches}")
