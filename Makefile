.PHONY: install test lint format

RELEASE_TYPE = Release
SRC = src

install:
	poetry install

test: install
	@PYTHONPATH=src poetry run pytest

lint:
	poetry run mypy $(SRC)
	poetry run ruff check $(SRC)
	poetry run ruff format --check $(SRC)

format:
	poetry run ruff format $(SRC)
	poetry run ruff check --fix $(SRC)
