from typing import Optional
import typer

from publicator import git, poetry, project

app = typer.Typer(name="publicator")

@app.command()
def cli(
    version: str = typer.Argument(..., metavar="version", help="can be one of (patch | minor | major | 1.2.3)"),
    repository: Optional[str] = typer.Option(default=None, metavar="name", help="Custom repository for publishing (must be specified in pyproject.toml)"),
    any_branch: bool = typer.Option(default=False, help="Allow publishing from any branch"),
    skip_clean: bool = typer.Option(default=False, help="Skip repository clean up"),
    yolo: bool = typer.Option(default=False, help="Skip reinstall and test steps"),
    skip_tag: bool = typer.Option(default=False, help="Skip creating a new tag"),
    skip_publish: bool = typer.Option(default=True, help="Skip publishing the package to the registry")
) -> None:
    current_branch = git.current_branch()
    release_branches = git.release_branches()

    if not any_branch:
        if not current_branch in git.release_branches():
            typer.echo(f"Current checked out branch {current_branch} is not a release branch {release_branches}")
            raise typer.Exit(code=1)

    if not skip_clean:
        if not git.is_working_directory_clean():
            typer.echo("Resetting working directory to a clean state")
            git.stash()
            git.pull()
            git.pop()

    if not yolo:
        typer.echo("Reinstalling dependencies")
        poetry.install()

        typer.echo("Running tests")
        poetry.run_tests()

    current_version = project.get_version()
    typer.echo(f"Bumping current version {current_version} to {version}")
    project.bump_version(version)

    typer.echo("Committing changes")
    poetry.ok()
    git.add()
    git.commit(f"release: {version}")

    if not skip_tag:
        typer.echo(f"Creating a new tag {version} from HEAD")
        git.create_tag(version, message=f"Version {version}")

    typer.echo("Building the package")
    poetry.build()

    typer.echo("Publishing the package to repository")
    poetry.publish(repository, dry_run=skip_publish)

    typer.echo("OK")
