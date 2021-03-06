PROJECT_NAME    = vishnu
PYTHON35        = python3.5
PYTHON27        = python2.7

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  tests      runs the unit tests"
	@echo "  dist       prepares for release"
	@echo "  release    makes the release"
	@echo "  clean      cleans the build environment"

.PHONY: test
test:
	python setup.py test

.PHONY: tests
tests:
	tox

.PHONY: coverage
coverage:
	py.test --cov-report term-missing:skip-covered --cov=vishnu tests

.PHONY: dist
dist:
	$(PYTHON27) setup.py sdist bdist_wheel

.PHONY: release
release:
	$(PYTHON27) setup.py sdist bdist_wheel upload

.PHONY: clean
clean:
	python setup.py clean
	if [ -a .eggs ]; then rm -rf .eggs; fi;
	if [ -a build ]; then rm -rf build; fi;
	if [ -a dist ]; then rm -rf dist; fi;
	if [ -a build ]; then rm -rf build; fi;
	if [ -a .tox ]; then rm -rf .tox; fi;
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
