Brief
=====

[![alt Latest Version](https://img.shields.io/pypi/v/lazyxml.svg)](https://pypi.org/project/lazyxml/)
[![alt License](https://img.shields.io/github/license/heronotears/lazyxml.svg)](https://github.com/heronotears/lazyxml/blob/master/LICENSE)
[![alt Downloads](https://img.shields.io/pypi/dm/lazyxml.svg)](https://pypi.org/project/lazyxml/)
[![Build Status](https://travis-ci.org/heronotears/lazyxml.svg?branch=master)](https://travis-ci.org/heronotears/lazyxml)

A simple xml parse and build library.


Installation
============

```sh
pip install lazyxml
```


Examples
========

* xml to python object

```sh
>>> import lazyxml
>>> xml = '<demo><foo>foo</foo><bar>bar</bar></demo>'
>>> lazyxml.loads(xml)
{'bar': 'bar', 'foo': 'foo'}
>>> lazyxml.loads(xml, strip_root=False)
{'demo': {'bar': 'bar', 'foo': 'foo'}}
>>> xml = '<demo><foo>foo</foo><bar>1</bar><bar>2</bar></demo>'
>>> lazyxml.loads(xml)
{'bar': ['1', '2'], 'foo': 'foo'}
```

* python object to xml

```sh
>>> data = {'demo':{'bar': ['1', '2'], 'foo': '<foo>'}}
>>> lazyxml.dumps(data)
'<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'
>>> lazyxml.dumps(data, cdata=False)
'<?xml version="1.0" encoding="utf-8"?><demo><foo>&lt;foo&gt;</foo><bar>1</bar><bar>2</bar></demo>'
>>> print lazyxml.dumps(data, indent=' ' * 4)
<?xml version="1.0" encoding="utf-8"?>
<demo>
   <foo><![CDATA[<foo>]]></foo>
   <bar><![CDATA[1]]></bar>
   <bar><![CDATA[2]]></bar>
</demo>
```


Documentation
=============

See [docs in readthedocs](http://lazyxml.readthedocs.org/en/latest/)


Changelog
=========

See [changelog](https://github.com/heronotears/lazyxml/blob/master/docs/changelog.rst)
