# Targets
install: pip-install
test: unit-test
lint: pylint
.PHONY: install test lint

# Directories
ROOT_DIR=$(shell pwd)
LIB_DIR=./lib
SRC_DIR=./src
TEST_DIR=./test
CONF_DIR=$(ROOT_DIR)/conf
ENV_DIR=$(LIB_DIR)/env
MODULES=$(SRC_DIR):$(TEST_DIR)

# Test directories
UNIT_TEST_DIR=$(TEST_DIR)/unit
SYSTEM_TEST_DIR=$(TEST_DIR)/system
INTEGRATION_TEST_DIR=$(TEST_DIR)/integration
WEBDRIVER_DIR=$(LIB_DIR)/selenium/webdrivers
CHROME_DRIVER_PID_FILE=$(WEBDRIVER_DIR)/pid.file
CHROME_DRIVER_LOG_FILE=$(WEBDRIVER_DIR)/log.file

# Configurations
CONFIG=$(CONF_DIR)/config

# Bootstrapers
LINT_CONFIG=$(CONF_DIR)/.pylint.rc
FLASK_SERVER=$(WEBSERVER_DIR)/server.py
REQUIREMENTS=$(LIB_DIR)/requirements.txt
COVERAGE_REPORT=$(TEST_DIR)/coverage.xml

# Binaries
SYSTEM_PIP=$(shell which pip3)
SYSTEM_XVFB=$(shell which Xvfb)
SYSTEM_PYTHON=$(shell which python3.5)
SYSTEM_VIRTUALENV=$(shell which virtualenv)

PIP=$(ENV_DIR)/bin/pip3
PYLINT=$(ENV_DIR)/bin/pylint
PYTHON=$(ENV_DIR)/bin/python3

# Flags
TEST_FILES=*_test.py
UNITTEST_FLAGS=-m unittest discover -p $(TEST_FILES) -s

# Environment variables
export PYTHONPATH=$(MODULES)
export PYTHONDONTWRITEBYTECODE=true

virtual-env-install:
	@$(SYSTEM_PIP) install virtualenv
	@$(SYSTEM_VIRTUALENV) -p $(SYSTEM_PYTHON) --no-site-packages $(ENV_DIR)

pip-install: virtual-env-install
pip-install:
	@$(PIP) install -r $(REQUIREMENTS)

flask: export BUSTORE_CONFIG=$(CONFIG)
flask:
	@$(PYTHON) $(FLASK_SERVER)

pylint:
	@$(PYLINT) --rcfile $(LINT_CONFIG) $(SRC_DIR)/*

unit-test: export BUSTORE_CONFIG=$(TEST_CONFIG)
unit-test:
	@$(PYTHON) $(UNITTEST_FLAGS) $(UNIT_TEST_DIR)

clean:
	-@find . -name '.DS_Store'   -delete
	-@find . -name '*.pyc'       -delete
	-@find . -name '__pycache__' -delete
