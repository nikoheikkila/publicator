import typer

from publicator import git, poetry

app = typer.Typer(name="publicator")

@app.command()
def cli(version: str = typer.Argument(...)) -> None:
    current_branch = git.current_branch()
    release_branches = git.release_branches()

    if not current_branch in git.release_branches():
        typer.echo(f"Current checked out branch {current_branch} is not a release branch {release_branches}")
        raise typer.Exit(code=1)

    if not git.is_working_directory_clean():
        typer.echo("Resetting working directory to a clean state")
        git.stash()
        git.pull()
        git.pop()

    typer.echo("Reinstalling dependencies")
    poetry.install()

    typer.echo("Running tests")
    poetry.run_tests()

    typer.echo("OK")
