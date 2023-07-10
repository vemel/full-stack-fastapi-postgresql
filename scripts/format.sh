#! /usr/bin/env bash

# Exit in case of error
set -e

poetry run isort \{\{cookiecutter.project_slug\}\}/backend
poetry run black \{\{cookiecutter.project_slug\}\}/backend
