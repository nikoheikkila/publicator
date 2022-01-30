#!/usr/bin/env bash
set -euo pipefail

echo "Installing pipx"
python3 -m pip install pipx --upgrade

echo "Cleaning old builds"
rm -rf dist

poetry build

for wheel in dist/*.whl; do
    echo "Installing from ${wheel}"
    pipx install --force "${wheel}"
done

echo "Testing executable"
publicator --version
publicator --help
