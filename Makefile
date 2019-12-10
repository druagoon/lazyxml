.PHONY: help

help:
	@echo 'Command:'
	@echo '     install      install package.'
	@echo '     pack         pack package locally.'
	@echo '     pypi         upload package to official pypi site.'
	@echo '     testpypi     upload package to test pypi site.'
	@echo '     ci           run unittest.'
	@echo '     clean        clean package useless files.'

install:
	python setup.py install

pack:
	python setup.py sdist bdist_wheel

pypi:
	twine upload dist/*

testpypi:
	twine upload --repository testpypi dist/*

ci:
	python -m unittest tests.test_parser && python -m unittest tests.test_builder

clean:
	rm -rf dist build lazyxml.egg-info
	find . -name '*.py[co]'|xargs rm -f
