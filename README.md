# Publicator

> A better `poetry publish`

## Features

### Supported

- Ensures you are publishing from your release branch (main and master by default)
- Ensures the working directory is clean and that there are no changes not pulled
- Reinstalls dependencies to ensure your project works with the latest dependency tree
- Ensures your Python version is supported by the project and its dependencies
- Runs the tests
- Bumps the version in pyproject.toml and creates a git tag
- Publishes the new version to pypi.org
- Pushes commits and tags (newly & previously created) to your Git server

### Upcoming

- Interactive UI
- Opens a prefilled GitHub Releases draft after publish
- See exactly what will be executed with preview mode, without pushing or publishing anything remotely

## Prerequisites

- Python 3.9 or later
- Poetry 1.1 or later
- Git 2.11 or later

## Install

Install with pipx.

```sh
pipx install publicator
```

## Usage

```plain
$ publicator --help

Usage:

$ publicator <version>

Version can be one of:
    patch | minor | major | 1.2.3

Options
    --any-branch            Allow publishing from any branch
    --branch                Name of the release branch (default: main | master)
    --no-tests              Skips tests
    --no-publish            Skips publishing
    --preview               Show tasks without actually executing them
    --no-release-draft      Skips opening a GitHub release draft
    --release-draft-only    Only opens a GitHub release draft
    --test-script           Name of shell command to run tests before publishing (default: `poetry run pytest`)
    --message               Version bump commit message. `%s` will be replaced with version. (default: '%s')
```

## Configuration

To be added later.
