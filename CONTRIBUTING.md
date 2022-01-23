# Contributing to Publicator

Issues and pull requests are most welcome.

To get started, fork this repository, clone it, and run `poetry install` to install it locally. Afterwards, the tool itself is usable through `poetry run publicator` or after activating the virtual environment with `poetry shell`.

The project uses [lefthook](https://github.com/evilmartians/lefthook) for development-time tasks. You can see the up-to-date pre-push and pre-commit configurations in the [configuration](lefthook.yml).

To verify your changes work, run the unit tests with `leftook run pre-push`. If you want to test building and running the real executable locally, run `./install.sh`.

Next, check the issues page or see if there's anything to improve in the existing codebase and start submitting your changes.
