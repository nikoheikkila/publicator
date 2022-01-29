import os
from typing import Optional
import typer

from publicator import git, github, poetry
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
    clean: bool = typer.Option(default=True, help="Ensure you're working with the latest changes"),
    tag: bool = typer.Option(default=True, help="Create a new tag for Git"),
    publish: bool = typer.Option(default=True, help="Publish the package to the registry"),
    push: bool = typer.Option(default=True, help="Push commits and tags to Git"),
    test_script: str = typer.Option(
        default="pytest", help="Name of the test script to run under the current virtual environment"
    ),
    template: str = typer.Option(
        default="release: %s", help="Commit message template (`%s` will be replaced with the new version tag)"
    ),
    release_draft: bool = typer.Option(
        default=True,
        help="Opens a pre-filled GitHub release page with browser if the current project is hosted on GitHub",
    ),
) -> None:
    if not any_branch:
        verify_branch()

    if clean:
        clean_up()
        install_dependencies()

    run_tests(test_script)

    new_version = bump_version(version)
    commit_changes(new_version, template)

    if tag:
        create_tag(new_version)

    build_package()

    if publish:
        publish_package(repository)

    if push:
        push_changes()

    if release_draft:
        draft_new_release(new_version)

    success("Published the new package version. Cheers!")


def info(message: str) -> None:
    typer.secho(f"📢 {message}", fg=typer.colors.BRIGHT_BLUE)


def success(message: str) -> None:
    typer.secho(f"🎉 {message}", fg=typer.colors.BRIGHT_GREEN, bold=True)


def fatal(message: str, exit_code: int = 1) -> None:
    typer.secho(f"❌ {message}", fg=typer.colors.BRIGHT_RED, bold=True)
    raise typer.Exit(code=exit_code)


def draft_new_release(tag: Semver) -> None:
    repo = git.Repo.from_remote()

    info("Opening GitHub release draft in browser")

    if preview:
        return

    try:
        url = github.new_release_url(repo, tag, title=f"Version {tag}", body="Write here")
        typer.launch(url)
    except github.ReleaseException as error:
        fatal(f"Skipping release draft. Reason: {error}")


def push_changes() -> None:
    info("Pushing changes to Git")
    if not preview:
        git.push()


def publish_package(repository: Optional[str]) -> None:
    info("Publishing the package to repository")
    if not preview:
        poetry.publish(repository)


def build_package() -> None:
    info("Building the package")
    if not preview:
        poetry.build()


def create_tag(version: Semver) -> None:
    info(f"Creating a new tag {version} from HEAD")
    if not preview:
        git.create_tag(version, message=f"Version {version}")


def commit_changes(semver: Semver, template: str) -> None:
    message = template % (semver)
    info(f'Committing changes with message: "{message}"')

    if not preview:
        poetry.ok()
        git.add()
        git.commit(message)


def bump_version(version: str) -> Semver:
    current_version = poetry.version()

    if preview:
        return current_version

    next_version = poetry.bump(version)
    info(f"Bumped version from {current_version} to {next_version}")

    return next_version


def run_tests(script: str) -> None:
    info(f"Running tests with '{script}'")
    if not preview:
        poetry.run(script)


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
