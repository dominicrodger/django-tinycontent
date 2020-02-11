.PHONY: clean docs lint test testall coverage release sdist

help:
	@echo "clean - remove build and Python artifacts"
	@echo "docs - build the documentation"
	@echo "lint - run flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf *.egg/
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -f pep8.txt
	rm -f coverage.xml
	rm -rf __pycache__

lint:
	flake8 tinycontent tests

test:
	python setup.py test

testall:
	tox

coverage:
	coverage run --source tinycontent setup.py test
	coverage report -m

release: clean lint testall
	twine upload -r pypi dist/*

sdist: clean
	python setup.py sdist
	ls -l dist

docs:
	tox -e docs
