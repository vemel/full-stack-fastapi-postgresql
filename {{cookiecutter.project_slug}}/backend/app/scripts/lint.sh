#!/usr/bin/env bash

set -x

mypy app
black app --check
isort --check-only --diff app
flake8
