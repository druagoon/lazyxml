# -*- coding: utf-8 -*-

"""A simple xml parse and build library.
"""

from __future__ import absolute_import, with_statement

from . import builder, parser

__title__ = 'lazyxml'
__description__ = 'A simple xml parse and build library.'
__author__ = 'Zonglong Fan'
__author_email__ = '<lazyboy.fan@gmail.com>'
__version__ = '1.3.2'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2014 Zonglong Fan'


def loads(content, encoding=None, unescape=False, strip_root=True,
          strip_attr=True, strip=True, errors='strict'):
    """Load xml content to python object.

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

    :param str content: xml content.
    :param str encoding: xml content encoding. if not set, will guess from xml header declare if possible.
    :param bool unescape: whether to unescape xml html entity character. Default to ``False``.
    :param bool strip_root: whether to strip root. Default to ``True``.
    :param bool strip_attr: whether to strip tag attrs. Default to ``True``.
    :param bool strip: whether to strip whitespace. Default to ``True``.
    :param string errors: the xml content decode error handling scheme. Default to ``strict``.
    :rtype: dict

    .. versionchanged:: 1.2.1
        The ``strip_attr`` option supported to decide whether return the element attributes for parse result.
    """
    return parser.Parser(encoding=encoding, unescape=unescape,
                         strip_root=strip_root, strip_attr=strip_attr,
                         strip=strip, errors=errors).xml2object(content)


def load(fp, encoding=None, unescape=False, strip_root=True,
         strip_attr=True, strip=True, errors='strict'):
    """Load xml content from file and convert to python object.

    >>> import lazyxml
    >>> with open('demo.xml', 'rb') as fp:
    >>>     lazyxml.load(fp)

    >>> from cStringIO import StringIO
    >>> buf = StringIO('<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>')
    >>> lazyxml.load(buf)
    {'bar': ['1', '2'], 'foo': '<foo>'}
    >>> buf.close()

    :param fp: a file or file-like object that support ``.read()`` to read the xml content
    :param str encoding: xml content encoding. if not set, will guess from xml header declare if possible.
    :param bool unescape: whether to unescape xml html entity character. Default to ``False``.
    :param bool strip_root: whether to strip root. Default to ``True``.
    :param bool strip_attr: whether to strip tag attrs. Default to ``True``.
    :param bool strip: whether to strip whitespace. Default to ``True``.
    :param string errors: the xml content decode error handling scheme. Default to ``strict``.
    :rtype: dict

    .. versionchanged:: 1.2.1
        The ``strip_attr`` option supported to decide whether return the element attributes for parse result.
    """
    content = fp.read()
    return loads(content, encoding=encoding, unescape=unescape,
                 strip_root=strip_root, strip_attr=strip_attr, strip=strip,
                 errors=errors)


def dumps(obj, encoding=None, header_declare=True, version=None, root=None,
          cdata=True, indent=None, ksort=False, reverse=False, errors='strict',
          hasattr=False, attrkey=None, valuekey=None):
    """Dump python object to xml.

    >>> import lazyxml

    >>> data = {'demo': {'foo': '<foo>', 'bar': ['1', '2']}}

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
    :param str encoding: xml content encoding. if not set, ``consts.Default.ENCODING`` used.
    :param bool header_declare: declare xml header. Default to ``True``.
    :param str version: xml version. if not set, ``consts.Default.VERSION`` used.
    :param str root: xml root. Default to ``None``.
    :param bool cdata: use cdata. Default to ``True``.
    :param str indent: xml pretty indent. Default to ``None``.
    :param bool ksort: sort xml element keys. Default to ``False``.
    :param bool reverse: sort xml element keys but reverse. Default to ``False``.
    :param str errors: xml content decode error handling scheme. Default to ``strict``.
    :param bool hasattr: data element has attributes. Default to ``False``.
    :param str attrkey: element tag attribute identification. if not set, ``consts.Default.KEY_ATTR`` used.
    :param str valuekey: element tag value identification. if not set, ``consts.Default.KEY_VALUE`` used.
    :rtype: str
    """
    return builder.Builder(encoding=encoding, header_declare=header_declare,
                           version=version, root=root, cdata=cdata,
                           indent=indent, ksort=ksort, reverse=reverse,
                           errors=errors, hasattr=hasattr, attrkey=attrkey,
                           valuekey=valuekey).object2xml(obj)


def dump(obj, fp, encoding=None, header_declare=True, version=None, root=None,
         cdata=True, indent=None, ksort=False, reverse=False, errors='strict',
         hasattr=False, attrkey=None, valuekey=None):
    """Dump python object to file.

    >>> import lazyxml
    >>> data = {'demo': {'foo': 1, 'bar': 2}}
    >>> lazyxml.dump(data, 'dump.xml')
    >>> with open('dump-fp.xml', 'w') as fp:
    >>>     lazyxml.dump(data, fp)

    >>> from cStringIO import StringIO
    >>> data = {'demo': {'foo': 1, 'bar': 2}}
    >>> buf = StringIO()
    >>> lazyxml.dump(data, buf)
    >>> buf.getvalue()
    <?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[1]]></foo><bar><![CDATA[2]]></bar></demo>
    >>> buf.close()

    :param obj: data for dump to xml.
    :param fp: a filename or a file or file-like object that support ``.write()`` to write the xml content.
    :param str encoding: xml content encoding. if not set, ``consts.Default.ENCODING`` used.
    :param bool header_declare: declare xml header. Default to ``True``.
    :param str version: xml version. if not set, ``consts.Default.VERSION`` used.
    :param str root: xml root. Default to ``None``.
    :param bool cdata: use cdata. Default to ``True``.
    :param str indent: xml pretty indent. Default to ``None``.
    :param bool ksort: sort xml element keys. Default to ``False``.
    :param bool reverse: sort xml element keys but reverse. Default to ``False``.
    :param str errors: xml content decode error handling scheme. Default to ``strict``.
    :param bool hasattr: data element has attributes. Default to ``False``.
    :param str attrkey: element tag attribute identification. if not set, ``consts.Default.KEY_ATTR`` used.
    :param str valuekey: element tag value identification. if not set, ``consts.Default.KEY_VALUE`` used.

    .. versionchanged:: 1.2
        The `fp` is a filename of string before this. It can now be a file or file-like object that support ``.write()`` to write the xml content.
    """
    xml = dumps(obj, encoding=encoding, header_declare=header_declare,
                version=version, root=root, cdata=cdata, indent=indent,
                ksort=ksort, reverse=reverse, errors=errors, hasattr=hasattr,
                attrkey=attrkey, valuekey=valuekey)
    func = getattr(fp, 'write', None)
    if func and callable(func):
        func(xml)
    else:
        with open(fp, 'w') as fobj:
            fobj.write(xml)
