#!/usr/bin/env python
# -*- coding: utf-8 -*-


# @package lazyxml
# @copyright Copyright (c) 2012, Zonglong Fan.
# @license MIT

r"""A simple xml parse and build lib.
"""


from __future__ import with_statement, absolute_import

from . import builder
from . import parser


__author__ = 'Zonglong Fan <lazyboy.fan@gmail.com>'
__version__ = '1.2.1'


def loads(content, **kw):
    r"""Load xml content to python object.

    >>> import lazyxml

    >>> xml = '<demo><foo>foo</foo><bar>bar</bar></demo>'
    >>> lazyxml.loads(xml)
    {'bar': 'bar', 'foo': 'foo'}

    >>> xml = '<demo><foo>foo</foo><bar>bar</bar></demo>'
    >>> lazyxml.loads(xml, strip_root=False)
    {'demo': {'bar': 'bar', 'foo': 'foo'}}

    >>> xml = '<demo><foo>foo</foo><bar>1</bar><bar>2</bar></demo>'
    >>> lazyxml.loads(xml)
    {'bar': ['1', '2'], 'foo': 'foo'}

    >>> xml = '<root xmlns:h="http://www.w3.org/TR/html4/">&lt;demo&gt;&lt;foo&gt;foo&lt;/foo&gt;&lt;bar&gt;bar&lt;/bar&gt;&lt;/demo&gt;</root>'
    >>> lazyxml.loads(xml, unescape=True, strip_root=False)
    {'root': {'demo': {'bar': 'bar', 'foo': 'foo'}}}

    :param content: xml content
    :type content: str

    ``kw`` arguments below here.

    :param encoding: XML编码 默认：``utf-8``.
    :param unescape: 是否转换HTML实体 默认：``False``.
    :type unescape: bool
    :param strip_root: 是否去除根节点 默认：``True``.
    :type strip_root: bool
    :param strip_attr: 是否去除节点属性 默认：``True``.
    :type strip_attr: bool
    :param strip: 是否去除空白字符（换行符、制表符） 默认：``True``.
    :type strip: bool
    :param errors: 解码错误句柄 参考: :meth:`str.decode` 默认：``strict``.
    :rtype: dict

    .. versionchanged:: 1.2.1
        The ``strip_attr`` option supported to decide whether return the element attributes for parse result.
    """
    return parser.Parser(**kw).xml2object(content)


def load(fp, **kw):
    r"""Load xml content from file and convert to python object.

    >>> import lazyxml
    >>> with open('demo.xml', 'rb') as fp:
    >>>     lazyxml.load(fp)

    >>> from cStringIO import StringIO
    >>> buffer = StringIO('<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>')
    >>> lazyxml.load(buffer)
    {'bar': ['1', '2'], 'foo': '<foo>'}
    >>> buffer.close()

    .. note::
        ``kw`` argument have the same meaning as in :func:`loads`

    :param fp: a file or file-like object that support ``.read()`` to read the xml content
    :rtype: dict
    """
    content = fp.read()
    return loads(content, **kw)


def dumps(obj, **kw):
    r"""Dump python object to xml.

    >>> import lazyxml

    >>> data = {'demo':{'foo': '<foo>', 'bar': ['1', '2']}}

    >>> lazyxml.dumps(data)
    '<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'

    >>> lazyxml.dumps(data, header_declare=False)
    '<demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'

    >>> lazyxml.dumps(data, cdata=False)
    '<?xml version="1.0" encoding="utf-8"?><demo><foo>&lt;foo&gt;</foo><bar>1</bar><bar>2</bar></demo>'

    >>> print lazyxml.dumps(data, indent=' ' * 4)
    <?xml version="1.0" encoding="utf-8"?>
    <demo>
        <foo><![CDATA[<foo>]]></foo>
        <bar><![CDATA[1]]></bar>
        <bar><![CDATA[2]]></bar>
    </demo>

    >>> lazyxml.dumps(data, ksort=True)
    '<?xml version="1.0" encoding="utf-8"?><demo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar><foo><![CDATA[<foo>]]></foo></demo>'

    >>> lazyxml.dumps(data, ksort=True, reverse=True)
    '<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'

    .. note::
        Data that has attributes convert to xml see ``demo/dump.py``.

    :param obj: data for dump to xml.

    ``kw`` arguments below here.

    :param encoding: XML编码 默认：``utf-8``.
    :param header_declare: 是否声明XML头部 默认：``True``.
    :type header_declare: bool
    :type version: XML版本号 默认：``1.0``.
    :param root: XML根节点 默认：``None``.
    :param cdata: 是否使用XML CDATA格式 默认：``True``.
    :type cdata: bool
    :param indent: XML层次缩进 默认：``None``.
    :param ksort: XML标签是否排序 默认：``False``.
    :type ksort: bool
    :param reverse: XML标签排序时是否倒序 默认：``False``.
    :type reverse: bool
    :param errors: 解码错误句柄 see: :meth:`str.decode` 默认：``strict``.
    :param hasattr: 是否包含属性 默认：``False``.
    :type hasattr: bool
    :param attrkey: 标签属性标识key 默认：``{attrs}``.
    :param valuekey: 标签值标识key 默认：``{values}``.
    :rtype: str
    """
    return builder.Builder(**kw).object2xml(obj)


def dump(obj, fp, **kw):
    r"""Dump python object to file.

    >>> import lazyxml
    >>> data = {'demo': {'foo': 1, 'bar': 2}}
    >>> lazyxml.dump(data, 'dump.xml')
    >>> with open('dump-fp.xml', 'w') as fp:
    >>>     lazyxml.dump(data, fp)

    >>> from cStringIO import StringIO
    >>> data = {'demo': {'foo': 1, 'bar': 2}}
    >>> buffer = StringIO()
    >>> lazyxml.dump(data, buffer)
    >>> buffer.getvalue()
    <?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[1]]></foo><bar><![CDATA[2]]></bar></demo>
    >>> buffer.close()

    .. note::
        ``kw`` argument have the same meaning as in :func:`dumps`

    :param obj: data for dump to xml.
    :param fp: a filename or a file or file-like object that support ``.write()`` to write the xml content

    .. versionchanged:: 1.2
        The `fp` is a filename of string before this. It can now be a file or file-like object that support ``.write()`` to write the xml content.
    """
    xml = dumps(obj, **kw)
    if isinstance(fp, basestring):
        with open(fp, 'w') as fobj:
            fobj.write(xml)
    else:
        fp.write(xml)
