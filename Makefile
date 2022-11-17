.DEFAULT: help
.PHONY: help bootstrap migrate serve lint inspect test testreport coverage outdated clean

help:
	@echo "Please use '$(MAKE) <target>' where <target> is one of the following:"
	@echo "  help        - show this text"
	@echo "  bootstrap   - initialize virtual environment and install project dependencies"
	@echo "  migrate     - run database migrations"
	@echo "  serve       - run the app in development mode"
	@echo "  lint        - inspect project source code for errors"
	@echo "  inspect     - inspect project source code for possible security errors"
	@echo "  test        - run project tests"
	@echo "  testreport  - run project tests and open HTML coverage report"
	@echo "  coverage    - run project tests and save coverage to XML file"
	@echo "  outdated    - list outdated project requirements"
	@echo "  clean       - clean up project environment and build artifacts"

bootstrap:
	poetry install

migrate:
	poetry run python -m alembic upgrade head

serve:
	GINSIDE_DEBUG=1 poetry run python -m uvicorn --reload ginside:app

lint:
	poetry run python -m flake8 tests ginside

inspect:
	poetry run python -m bandit -r ginside

test:
	poetry run python -m pytest --cov-report=term-missing

testreport:
	poetry run python -m pytest --cov-report=html
	@xdg-open htmlcov/index.html || open htmlcov/index.html || echo "Coverage is available at htmlcov/index.html"

coverage:
	poetry run python -m pytest --cov-report=xml

outdated:
	poetry run python -m pip list --outdated --format=columns

clean:
	rm -rf .pytest_cache htmlcov .coverage coverage.xml
