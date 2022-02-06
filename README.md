<h1>🗞 Publicator</h1>

> A better `poetry publish` experience.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/publicator)
![PyPI](https://img.shields.io/pypi/v/publicator)
![PyPI - Downloads](https://img.shields.io/pypi/dm/publicator)
![PyPI - License](https://img.shields.io/pypi/l/publicator)
[![Application Test Suite](https://github.com/nikoheikkila/publicator/actions/workflows/python-package.yml/badge.svg)](https://github.com/nikoheikkila/publicator/actions/workflows/python-package.yml)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/publicator)

While [Poetry](https://python-poetry.org) finally brings us a sane solution for publishing and maintaining Python packages, many developers crave for a more _enhanced_ and safer user experience. Publicator aims to offer a convenient method for publishing your everyday libraries.

Publicator has been inspired by Sindre Sorhus' excellent [`np`](https://github.com/sindresorhus/np) package for Node.js ecosystem and graciously funded by [**Futurice Spice Program**](https://spiceprogram.org).

<h2>Table of Contents</h2>

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Install](#install)
* [Usage](#usage)
  * [Configuration](#configuration)
  * [Preview Mode (Dry-Run)](#preview-mode-dry-run)
  * [Shell Completion](#shell-completion)
* [Contributing](#contributing)

## Features

* Ensures you are publishing from your release branch (`main` and `master` by default)
* Ensures the working directory is clean and latest changes are pulled
* Reinstalls dependencies to ensure your project works with the latest dependency tree
* Ensures your Python version is supported by the project and its dependencies
* Runs the tests with custom test script
* Bumps the version in `pyproject.toml` and creates a Git tag based on it
* Publishes the new version to [Python Package Index](https://pypi.org) or custom repository
* Pushes commits and tags (newly & previously created) to your Git server
* If the project is hosted on GitHub opens a prefilled GitHub Releases draft after publishing
* Fully configurable via command-line arguments or the `pyproject.toml` file
* See what will be executed with preview mode, without pushing or publishing anything remotely

## Prerequisites

* **Python 3.8** or later
* **Poetry 1.1** or later
* **Git 2.11** or later

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

Publicator takes one command-line argument indicating the suitable version bump. It follows semantic versioning rules accurately.

```sh
# Release a new patch version (e.g. 1.0.0 -> 1.0.1)
publicator patch

# Release a new minor version (e.g. 1.0.1 -> 1.1.0)
publicator minor

# Release a new major version (e.g. 1.1.0 -> 2.0.0)
publicator major
```

Run `publicator --help` to see the full list of supported options:

```plain
$ publicator --help

Usage: publicator [OPTIONS] version

  Handles publishing a new Python package via Poetry safely and conveniently.

Arguments:
  version  can be a valid semver or one of: patch, minor, major, prepatch,
           preminor, premajor, prerelease  [required]

Options:
  -V, --version
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
  --test-script TEXT              Name of the test script to run under the
                                  current virtual environment  [default:
                                  pytest -x --assert=plain]
  --template TEXT                 Commit message template (`%s` will be
                                  replaced with the new version tag)
                                  [default: release: %s]
  --release-draft / --no-release-draft
                                  Opens a pre-filled GitHub release page with
                                  browser if the current project is hosted on
                                  GitHub  [default: release-draft]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

### Configuration

Publicator follows the pleasantly Pythonic way of specifying the configuration within `pyproject.toml` file. Below are the default configuration values.

```toml
[tool.publicator]
any-branch    = false
clean         = true
publish       = true
push          = true
release-draft = true
tag           = true
template      = "release: %s"
```

Values passed as command-line arguments take precedence over configuration file values.

Configuration enables for more granular usage. For example, in CI/CD pipelines you might want to disable publishing the package to registry or disable creating Git tags depending on your use case.

### Preview Mode (Dry-Run)

If you'd rather skip on everything and check what would be executed, you can activate a preview mode via environment variable like so:

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
