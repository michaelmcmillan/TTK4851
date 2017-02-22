# Targets
install: pip-install
unit-test: test
.PHONY: install test

# Directories
SRC_DIR=./src
ENV_DIR=./env
TEST_DIR=./test
MODULES=$(SRC_DIR):$(TEST_DIR)

# Tests
TEST_FILES=*_test.py
UNITTEST_FLAGS=-m unittest discover -p $(TEST_FILES) -s

# Bootstrapers
REQUIREMENTS=./requirements.txt

# Binaries
SYSTEM_PIP=$(shell which pip)
SYSTEM_XVFB=$(shell which Xvfb)
SYSTEM_PYTHON=$(shell which python)
SYSTEM_VIRTUALENV=$(shell which virtualenv)

PIP=$(ENV_DIR)/bin/pip
PYTHON=$(ENV_DIR)/bin/python

test:
	@$(PYTHON) $(UNITTEST_FLAGS) $(TEST_DIR)

# Environment variables
export PYTHONPATH=$(MODULES)
export PYTHONDONTWRITEBYTECODE=true

virtual-env-install:
	@$(SYSTEM_VIRTUALENV) -p $(SYSTEM_PYTHON) --no-site-packages $(ENV_DIR)

pip-install: virtual-env-install
pip-install:
	@$(PIP) install -r $(REQUIREMENTS)

clean:
	-@find . -name '.DS_Store'   -delete
	-@find . -name '*.pyc'       -delete
	-@find . -name '__pycache__' -delete
