# -*- coding: utf-8 -*-

#  MIT License
#
#  Copyright (c) 2019 Ryan Fau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import cgi
import collections
import types

from . import utils
from .consts import Default


class Builder(object):
    """Simple xml builder
    """

    def __init__(self, encoding=None, header_declare=True, version=None,
                 root=None, cdata=True, indent=None, ksort=False, reverse=False,
                 errors='strict', hasattr=False, attrkey=None, valuekey=None):
        """Constructor for Builder, with sensible defaults.

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
        """
        self.__encoding = encoding or Default.ENCODING
        self.__header_declare = header_declare
        self.__version = version or Default.VERSION
        self.__root = root
        self.__cdata = cdata
        self.__indent = indent
        self.__ksort = ksort
        self.__reverse = reverse
        self.__errors = errors
        self.__hasattr = hasattr
        self.__attrkey = attrkey or Default.KEY_ATTR
        self.__valuekey = valuekey or Default.KEY_VALUE
        self.__tree = []

    def dict2xml(self, data):
        """Convert dict to xml.

        .. warning::
            **DEPRECATED:** :meth:`dict2xml` is deprecated. Please use :meth:`object2xml` instead.

        .. deprecated:: 1.2
        """
        return self.object2xml(data)

    def object2xml(self, data):
        """Convert python object to xml string.

        :param data: data for build xml. If don't provide the ``root`` option, type of ``data`` must be dict and ``len(data) == 1``.
        :rtype: str or unicode

        .. versionadded:: 1.2
        """
        if self.__header_declare:
            self.__tree.append(
                self.build_xml_header(self.__encoding, self.__version))

        root = self.__root
        if not root:
            assert (isinstance(data, collections.Mapping) and len(data) == 1), \
                'if root not specified, the data that dict object and length must be one required.'
            root, data = data.items()[0]

        self.build_tree(data, root)
        xml = unicode(''.join(self.__tree).strip())

        if self.__encoding != Default.ENCODING:
            xml = xml.encode(self.__encoding, errors=self.__errors)
        return xml

    @staticmethod
    def build_xml_header(encoding=None, version=None):
        """Build xml header include version and encoding.
        """
        return '<?xml version="{}" encoding="{}"?>'.format(
            version or Default.VERSION, encoding or Default.ENCODING)

    def build_tree(self, data, tagname, attrs=None, depth=0):
        """Build xml tree.

        :param data: data for build xml.
        :param tagname: element tag name.
        :param attrs: element attributes. Default：``None``.
        :type attrs: dict or None
        :param depth: element depth of the hierarchy. Default：``0``.
        :type depth: int
        """
        if data is None:
            data = ''
        indent = ('\n%s' % (self.__indent * depth)) if self.__indent else ''
        if isinstance(data, collections.Mapping):
            if self.__hasattr and self.check_structure(data.keys()):
                attrs, values = self.pickdata(data)
                self.build_tree(values, tagname, attrs, depth)
            else:
                self.__tree.append(
                    '{}{}'.format(indent, self.tag_start(tagname, attrs)))
                iter = data.iteritems()
                if self.__ksort:
                    iter = sorted(iter, key=lambda x: x[0],
                                  reverse=self.__reverse)
                for k, v in iter:
                    attrs = {}
                    if (self.__hasattr and isinstance(v, collections.Mapping)
                            and self.check_structure(v.keys())):
                        attrs, v = self.pickdata(v)
                    self.build_tree(v, k, attrs, depth + 1)
                self.__tree.append('{}{}'.format(indent, self.tag_end(tagname)))
        elif utils.is_iterable(data) and not isinstance(data, types.StringTypes):
            for v in data:
                self.build_tree(v, tagname, attrs, depth)
        else:
            self.__tree.append(indent)
            data = self.safedata(data, self.__cdata)
            self.__tree.append(self.build_tag(tagname, data, attrs))

    def check_structure(self, keys):
        """Check structure availability by ``attrkey`` and ``valuekey`` option.
        """
        return set(keys) <= {self.__attrkey, self.__valuekey}

    def pickdata(self, data):
        """Pick data from ``attrkey`` and ``valuekey`` option.

        :return: a pair of (attrs, values)
        :rtype: tuple
        """
        attrs = data.get(self.__attrkey) or {}
        values = data.get(self.__valuekey) or ''
        return (attrs, values)

    @staticmethod
    def safedata(data, cdata=True):
        """Convert xml special chars to entities.

        :param data: the data will be converted safe.
        :param cdata: whether to use cdata. Default：``True``. If not, use :func:`cgi.escape` to convert data.
        :type cdata: bool
        :rtype: str
        """
        if cdata:
            return '<![CDATA[{}]]>'.format(data)
        return cgi.escape(str(data), True)

    @classmethod
    def build_tag(cls, tag, text='', attrs=None):
        """Build tag full info include the attributes.

        :param tag: tag name.
        :param text: tag text.
        :param attrs: tag attributes. Default：``None``.
        :type attrs: dict or None
        :rtype: str
        """
        return '{}{}{}'.format(cls.tag_start(tag, attrs), text,
                               cls.tag_end(tag))

    @staticmethod
    def build_attr(attrs):
        """Build tag attributes.

        :param attrs: tag attributes
        :type attrs: dict
        :rtype: str
        """
        attrs = sorted(attrs.iteritems(), key=lambda x: x[0])
        return ' '.join(['{}="{}"'.format(k, v) for k, v in attrs])

    @classmethod
    def tag_start(cls, tag, attrs=None):
        """Build started tag info.

        :param tag: tag name
        :param attrs: tag attributes. Default：``None``.
        :type attrs: dict or None
        :rtype: str
        """
        if attrs:
            return '<{} {}>'.format(tag, cls.build_attr(attrs))
        return '<{}>'.format(tag)

    @staticmethod
    def tag_end(tag):
        """Build closed tag info.

        :param tag: tag name
        :rtype: str
        """
        return '</{}>'.format(tag)
