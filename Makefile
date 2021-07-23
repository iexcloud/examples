yield_curve:  ## Run the yield curve app
	python -m iexexamples.dash.yield_curve

timeseries_downloader: ## Run the timerseries downloader app
	python -m iexexamples.dash.timeseries_downloader

tests: ## Make unit tests
	python -m pytest -v iexexamples --cov=iexexamples --junitxml=python_junit.xml --cov-report=xml --cov-branch

lint: ## run linter
	python -m flake8 iexexamples setup.py

fix:  ## run black fix
	python -m black iexexamples/ setup.py

clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf 
	find . -name "*.pyc" | xargs rm -rf 
	rm -rf .coverage cover htmlcov logs build dist *.egg-info
	# make -C ./docs clean
	# rm -rf ./docs/*.*.rst  # generated

docs:  ## make documentation
	make -C ./docs html
	open ./docs/_build/html/index.html

install:  ## install to site-packages
	python -m pip install .

dev:
	python -m pip install .[dev]

dist:  ## create dists
	rm -rf dist build
	python setup.py sdist bdist_wheel
	python -m twine check dist/*
	
publish: dist  ## dist to pypi
	python -m twine upload dist/* --skip-existing

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean test tests help docs dist
