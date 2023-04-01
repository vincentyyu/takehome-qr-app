.PHONY: all venv run run-dashboard clean lint test

# Define variables
ENV ?= dev
VENV_DIR := .venv_$(ENV)

# venv module paths
VENV_ACTIVATE := $(VENV_DIR)/bin/activate
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
PRECOMMIT := $(VENV_DIR)/bin/pre-commit
BLACK := $(VENV_DIR)/bin/black
AUTOFLAKE := $(VENV_DIR)/bin/autoflake
FLAKE := $(VENV_DIR)/bin/flake8
ISORT := $(VENV_DIR)/bin/isort
PYTEST := $(VENV_DIR)/bin/pytest

# Default target
all: venv

# Create a virtual environment
venv: $(VENV_DIR)
$(VENV_DIR): requirements.txt requirements-dev.txt
ifeq (,$(wildcard $(VENV_DIR)))
	@echo "Creating virtual environment for $(ENV) environment..."
	@python3 -m venv $(VENV_DIR)
	@echo "Installing dependencies for $(ENV) environment..."
	@$(PIP) install -U pip
	@$(PIP) install wheel setuptools
ifeq ($(ENV),dev)
	@$(PIP) install -r requirements-dev.txt
	@$(PRECOMMIT) install
else
	@$(PIP) install -r requirements.txt
endif
	@$(PIP) install .
endif

# Run the main pipeline and spin up dashboards with arguments
run: venv
	@echo "Running data pipeline with arguments: $(ARGS)"
	@$(PYTHON) src/pipeline.py $(ARGS)
	@echo "Data pipeline run complete. Starting dashboard..."
	@$(MAKE) --no-print-directory -s run-dashboard

run-dashboard: venv
	@$(PYTHON) src/reporting/dashboard.py

# Lint the codes
lint: venv
	@echo "Running linting using Black, Autoflake, Flake8, and isort..."
	@$(AUTOFLAKE) src tests
	@$(BLACK) src tests
	@$(FLAKE) src tests
	@$(ISORT) src tests

# Run tests and generate coverage report
test: venv
	@echo "Running tests with pytest and generating coverage report..."
	@$(PYTEST)

# Clean the virtual environment and other generated files
clean:
	@echo "Cleaning up..."
	@rm -rf .venv_dev .venv_prod .pytest_cache htmlcov .coverage
	@find . -type d -name "__pycache__" -exec rm -rf {} +
