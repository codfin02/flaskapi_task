#!/bin/bash

set -eo pipefail

COLOR_GREEN=`tput setaf 2;`
COLOR_NC=`tput sgr0;` # No Color

echo "Starting black"
python3 -m poetry run black .
echo "OK"

echo "Starting ruff"
python3 -m poetry run ruff check --select I --fix
python3 -m poetry run ruff check --fix
echo "OK"

echo "Starting mypy"
python3 -m poetry run mypy .
echo "OK"

echo "Starting pytest with coverage"
python3 -m poetry run coverage run -m pytest .
python3 -m poetry run coverage report -m
python3 -m poetry run coverage html

echo "${COLOR_GREEN}All tests passed successfully!${COLOR_NC}" 