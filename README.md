# 🗞 Publicator

> A better `poetry publish` experience.

While [Poetry](https://python-poetry.org) finally brings us a sane solution for publishing and maintaining Python packages, many developers crave for a more _enhanced_ and safer user experience. Publicator aims to offer a convenient tool for everyday work.

Licensed under [**MIT**](LICENSE.md).

## Features

### Supported

- Ensures you are publishing from your release branch (`main` and `master` by default)
- Ensures the working directory is clean and latest changes are pulled
- Reinstalls dependencies to ensure your project works with the latest dependency tree
- Ensures your Python version is supported by the project and its dependencies
- Runs the tests
- Bumps the version in `pyproject.toml` and creates a Git tag based on it
- Publishes the new version to [Python Package Index](https://pypi.org) or custom repository
- Pushes commits and tags (newly & previously created) to your Git server
- See what will be executed with preview mode, without pushing or publishing anything remotely

### Planned

- Open a prefilled GitHub Releases draft after publishing

## Prerequisites

- **Python 3.8** or later
- **Poetry 1.1** or later
- **Git 2.11** or later

## Install

Install or run directly using `pipx`, which manages an isolated virtual environment for you.

```sh
pipx install publicator
pipx run publicator <version>
```

Alternatively, add it as dependency to your Poetry project.

```sh
poetry add --dev publicator
poetry run publicator <version>
```

## Usage

```sh
$ publicator --help

Usage: publicator [OPTIONS] version

Arguments:
  version  can be a valid semver or one of: patch, minor, major, prepatch,
           preminor, premajor, prerelease  [required]

Options:
  --repository name               Custom repository for publishing (must be
                                  specified in pyproject.toml)
  --any-branch / --no-any-branch  Allow publishing from any branch  [default:
                                  no-any-branch]
  --clean / --no-clean            Ensure you are working with the latest
                                  changes  [default: clean]
  --tag / --no-tag                Create a new tag for Git  [default: tag]
  --publish / --no-publish        Publish the package to the registry
                                  [default: publish]
  --push / --no-push              Push commits and tags to Git  [default:
                                  push]
  --test-script TEXT              Name of the test script to run under the
                                  current virtual environment  [default:
                                  pytest]
  --template TEXT                 Commit message template (`%s` will be
                                  replaced with the new version tag)
                                  [default: release: %s]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

### Configuration

Flags described above enable more granular usage. For example, in CI/CD pipelines you might want to disable publishing the package to registry or disable creating Git tags depending on your use case.

If you'd rather skip on everything and check what would be executed (_dry run_), you can activate a preview mode via environment variable like so:

```sh
PUBLICATOR_PREVIEW=true publicator <version>
```

### Shell Completion

Publicator stands on the shoulders of [Typer](https://typer.tiangolo.com), which is a robust CLI library for Python. You can generate <kbd>TAB</kbd> completions for common shells such as Bash, ZSH, Fish, and Powershell.

```sh
publicator --install-completion <shell>
```

## Contributing

See [**here**](CONTRIBUTING.md) for instructions.
