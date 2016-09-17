PROJ_NAME   = prestans3
PYTHON35    = python3.5
PTYHON27    = python2.7

.PHONY: clean
tests:
	tox

.PHONY: dist
dist:
	$(PTYHON27) setup.py sdist bdist_wheel

.PHONY: release
release:
	$(PTYHON27) setup.py sdist bdist_wheel upload

.PHONY: clean
clean:
	python setup.py clean
	if [ -a .eggs ]; then rm -rf .eggs; fi;
	if [ -a build ]; then rm -rf build; fi;
	if [ -a dist ]; then rm -rf dist; fi;
	if [ -a build ]; then rm -rf build; fi;
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
