.PHONY: help

help:
	@echo 'Command:'
	@echo 'install    install the package.'
	@echo 'pack       pack the package only in local.'
	@echo 'upload     upload package to official pypi site.'
	@echo 'test       upload packge to test pypi site.'
	@echo 'clean      clean package files.'

install:
	python setup.py install

pack:
	python setup.py sdist --formats=gztar

upload:
	python setup.py sdist --formats=gztar register upload

test:
	python setup.py sdist --formats=gztar register -r pypitest upload -r pypitest

clean:
	rm -rf dist lazyxml.egg-info build
	find . -name '*.py[co]'|xargs rm -f
