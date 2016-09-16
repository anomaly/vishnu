PROJ_NAME   = prestans3
PYTHON35    = python3.5

.PHONY: clean
tests:
	tox

.PHONY: dist
dist:
	$(PYTHON35) setup.py sdist bdist_wheel

.PHONY: release
release:
	$(PYTHON35) setup.py sdist bdist_wheel upload

.PHONY: clean
clean:
	python setup.py clean
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
