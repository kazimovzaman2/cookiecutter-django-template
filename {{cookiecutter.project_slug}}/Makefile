help:
	@echo "-----------------HELP-----------------"
	@echo "This project requires uv for building."
	@echo "make install: installs the project dependencies (no dev)."
	@echo "make install-dev: installs the project dependencies (with dev)."
	@echo "make run: runs the project."
	@echo "make celery: runs celery"
	@echo "make celery-flower: runs celery flower"
	@echo "make celery-beat: runs celery beat"
	@echo "make shell: runs django shell."
	@echo "make makemigrations: creates migrations for all apps."
	@echo "make migrate: applies all migrations."
	@echo "make format: formats the code to pass required standards."
	@echo "make spelling: run code spelling check."
	@echo "make type: tests types with mypy."
	@echo "make test: runs tests."
	@echo "make test-cov: runs tests with coverage and writes report."
	@echo "--------------------------------------"

install: uv.lock
	uv sync

install-dev: uv.lock
	uv sync --dev

run:
	uv run manage.py runserver

celery:
	uv run celery -A config worker -l info

celery-flower:
	uv run celery -A config flower -l info

celery-beat:
	uv run celery -A config beat -l info

shell:
	uv run manage.py

makemigrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

format:
	ruff check --fix-only --exit-zero
	ruff format

spelling:
	uv run codespell

type:
	uv run mypy .

test:
	uv run pytest

test-cov:
	uv run coverage run -m pytest
	uv run coverage report
	uv run coverage html
