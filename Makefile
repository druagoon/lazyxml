pack:
	python setup.py sdist --formats=gztar

install:
	python setup.py install

upload:
	python setup.py sdist --formats=gztar register upload

test:
	python setup.py sdist --formats=gztar register -r pypitest upload -r pypitest

clean:
	rm -rf dist lazyxml.egg-info build
	find . -name '*.py[co]'|xargs rm -f
