.DEFAULT: help
.PHONY: help bootstrap lint test testreport outdated clean

help:
	@echo "Please use '$(MAKE) <target>' where <target> is one of the following:"
	@echo "  help        - show this text"
	@echo "  bootstrap   - initialize virtual environment and install project dependencies"
	@echo "  lint        - inspect project source code for errors"
	@echo "  test        - run project tests"
	@echo "  testreport  - run project tests and open HTML coverage report"
	@echo "  outdated    - list outdated project requirements"
	@echo "  clean       - clean up project environment and build artifacts"

bootstrap:
	poetry install

lint:
	poetry run python -m flake8 tests ginside

test:
	poetry run pytest --cov-report=term-missing

testreport:
	poetry run pytest --cov-report=html
	xdg-open htmlcov/index.html || echo "Coverage is available at htmlcov/index.html"

outdated:
	poetry run python -m pip list --outdated --format=columns

clean:
	rm -rf .pytest_cache htmlcov .coverage
