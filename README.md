# 🗞 Publicator

> A better `poetry publish` experience.

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

Install with pipx.

```sh
pipx install publicator
```

## Usage

```plain
Usage: publicator [OPTIONS] version

Arguments:
  version  can be a valid semver or one of: patch, minor, major, prepatch,
           preminor, premajor, prerelease  [required]

Options:
  --repository name               Custom repository for publishing (must be
                                  specified in pyproject.toml)
  --any-branch / --no-any-branch  Allow publishing from any branch  [default:
                                  no-any-branch]
  --clean / --no-clean            Ensure you're working with the latest
                                  changes  [default: clean]
  --tag / --no-tag                Create a new tag for Git  [default: tag]
  --publish / --no-publish        Publish the package to the registry
                                  [default: publish]
  --push / --no-push              Push commits and tags to Git  [default:
                                  push]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

## Contributing

See [**here**](CONTRIBUTING.md) for instructions.
