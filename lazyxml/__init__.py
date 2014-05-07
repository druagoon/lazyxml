#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
lazyxml: a simple xml parse and build lib.

@package
@copyright Copyright (c) 2012, Zonglong Fan.
@license
"""


from __future__ import with_statement, absolute_import
from .parser import Parser
from .builder import Builder

__author__ = 'Zonglong Fan <lazyboy.fan@gmail.com>'
__version__ = '1.1.0'


def loads(content, **kw):
    return Parser(**kw).xml2dict(content)


def load(fp, **kw):
    """
    # @param object fp a file or file-like object that has ``.read()`` method to get the xml content
    """
    content = fp.read()
    return loads(content, **kw)


def dumps(obj, **kw):
    return Builder(**kw).dict2xml(obj)


def dump(obj, filename, **kw):
    xml = dumps(obj, **kw)
    with open(filename, 'wb') as fp:
        fp.write(xml)
    return True
