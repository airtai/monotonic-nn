#!/bin/bash
set -e

echo "Running mypy..."
mypy airt tests docs/*.py docs/docs_src examples

echo "Running bandit..."
bandit -c pyproject.toml -r airt

echo "Running semgrep..."
semgrep scan --config auto --error
