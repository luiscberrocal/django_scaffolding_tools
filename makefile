sources = django_scaffolding_tools

.PHONY: test format lint unittest coverage pre-commit clean
test: unittest


unittest:
	pytest

coverage:
	pytest --cov=$(sources) --cov-branch --cov-report=term-missing tests

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf .pytest_cache
	rm -rf *.egg-info
	rm -rf .tox dist site
	rm -rf coverage.xml .coverage

dist: clean
	poetry build

release: dist ## package and upload a release
	twine upload dist/*
