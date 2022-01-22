from typing import Optional
import typer

from publicator import git, poetry, project
from publicator.semver import Semver

app = typer.Typer(name="publicator")

@app.command()
def cli(
    version: str = typer.Argument(..., metavar="version", help="can be one of (patch | minor | major | 1.2.3)"),
    repository: Optional[str] = typer.Option(default=None, metavar="name", help="Custom repository for publishing (must be specified in pyproject.toml)"),
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

    semver = bump_version(version)
    commit_changes(semver)

    if not skip_tag:
        create_tag(version)

    build_package()

    if not skip_publish:
        publish_package(repository, skip_publish)

    if not skip_push:
        push()

    typer.echo("OK")

def push():
    typer.echo("Pushing changes to Git")
    git.push()

def publish_package(repository: str, skip_publish: bool) -> None:
    typer.echo("Publishing the package to repository")
    poetry.publish(repository, dry_run=skip_publish)

def build_package() -> None:
    typer.echo("Building the package")
    poetry.build()

def create_tag(version: Semver) -> None:
    typer.echo(f"Creating a new tag {version} from HEAD")
    git.create_tag(version, message=f"Version {version}")

def commit_changes(semver: Semver) -> None:
    typer.echo("Committing changes")
    poetry.ok()
    git.add()
    git.commit(f"release: {semver}")

def bump_version(version: str) -> Semver:
    current_version = project.get_version()
    typer.echo(f"Bumping current version {current_version} to {version}")

    return project.bump_version(version)

def run_tests():
    typer.echo("Running tests")
    poetry.run_tests()

def install_dependencies():
    typer.echo("Reinstalling dependencies")
    poetry.install()

def clean_up() -> None:
    if git.is_working_directory_clean():
        return

    typer.echo("Resetting working directory to a clean state")
    git.stash()
    git.pull()
    git.pop()

def verify_branch() -> None:
    current_branch = git.current_branch()
    release_branches = git.release_branches()

    if not current_branch in release_branches:
        typer.echo(f"Current checked out branch {current_branch} is not a release branch {release_branches}")
        raise typer.Exit(code=1)
