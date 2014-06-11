#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cgi

import utils


class Builder(object):
    r"""XML Builder
    """

    def __init__(self, **kw):
        self.__encoding = 'utf-8'           # 内部默认编码: utf-8

        self.__options = {
            'encoding': None,               # XML编码
            'header_declare': True,         # 是否声明XML头部
            'version': '1.0',               # XML版本号
            'root': None,                   # XML根节点
            'cdata': True,                  # 是否使用XML CDATA格式
            'indent': None,                 # XML层次缩进
            'ksort': False,                 # XML标签是否排序
            'reverse': False,               # XML标签排序时是否倒序
            'errors': 'strict',             # 编码错误句柄 参见: Codec Base Classes
            'hasattr': False,               # 是否包含属性
            'attrkey': '{attrs}',           # 标签属性标识key
            'valuekey': '{values}'          # 标签值标识key
        }

        self.__tree = []
        self.set_options(**kw)

    def set_options(self, **kw):
        r"""Set Builder options.

        .. seealso::
            ``kw`` argument have the same meaning as in :func:`lazyxml.dumps`
        """
        for k, v in kw.iteritems():
            if k in self.__options:
                self.__options[k] = v

    def get_options(self):
        r"""Get Builder options.
        """
        return self.__options

    def dict2xml(self, data):
        r"""Convert dict to xml.

        .. warning::
            **DEPRECATED:** :meth:`dict2xml` is deprecated. Please use :meth:`object2xml` instead.

        .. deprecated:: 1.2
        """
        return self.object2xml(data)

    def object2xml(self, data):
        r"""Convert python object to xml string.

        :param data: data for build xml. If don't provide the ``root`` option, type of ``data`` must be dict and ``len(data) == 1``.
        :rtype: str or unicode

        .. versionadded:: 1.2
        """
        if not self.__options['encoding']:
            self.set_options(encoding=self.__encoding)

        if self.__options['header_declare']:
            self.__tree.append(self.build_xml_header())

        root = self.__options['root']
        if not root:
            assert (isinstance(data, utils.DictTypes) and len(data) == 1), \
                'if root not specified, the data that dict object and length must be one required.'
            root, data = data.items()[0]

        self.build_tree(data, root)
        xml = unicode(''.join(self.__tree).strip())

        if self.__options['encoding'] != self.__encoding:
            xml = xml.encode(self.__options['encoding'], errors=self.__options['errors'])
        return xml

    def build_xml_header(self):
        r"""Build xml header include version and encoding.

        :rtype: str
        """
        return '<?xml version="%s" encoding="%s"?>' % (self.__options['version'], self.__options['encoding'])

    def build_tree(self, data, tagname, attrs=None, depth=0):
        r"""Build xml tree.

        :param data: data for build xml.
        :param tagname: element tag name.
        :param attrs: element attributes. Default：``None``.
        :type attrs: dict or None
        :param depth: element depth of the hierarchy. Default：``0``.
        :type depth: int
        """
        if data is None:
            data = ''
        indent = ('\n%s' % (self.__options['indent'] * depth)) if self.__options['indent'] else ''
        if isinstance(data, utils.DictTypes):
            if self.__options['hasattr'] and self.check_structure(data.keys()):
                attrs, values = self.pickdata(data)
                self.build_tree(values, tagname, attrs, depth)
            else:
                self.__tree.append('%s%s' % (indent, self.tag_start(tagname, attrs)))
                iter = data.iteritems()
                if self.__options['ksort']:
                    iter = sorted(iter, key=lambda x:x[0], reverse=self.__options['reverse'])
                for k, v in iter:
                    attrs = {}
                    if self.__options['hasattr'] and isinstance(v, utils.DictTypes) and self.check_structure(v.keys()):
                        attrs, v = self.pickdata(v)
                    self.build_tree(v, k, attrs, depth+1)
                self.__tree.append('%s%s' % (indent, self.tag_end(tagname)))
        elif utils.is_iterable(data):
            for v in data:
                self.build_tree(v, tagname, attrs, depth)
        else:
            self.__tree.append(indent)
            data = self.safedata(data, self.__options['cdata'])
            self.__tree.append(self.build_tag(tagname, data, attrs))

    def check_structure(self, keys):
        r"""Check structure availability by ``attrkey`` and ``valuekey`` option.
        """
        return set(keys) <= set([self.__options['attrkey'], self.__options['valuekey']])

    def pickdata(self, data):
        r"""Pick data from ``attrkey`` and ``valuekey`` option.

        :return: a pair of (attrs, values)
        :rtype: tuple
        """
        attrs = data.get(self.__options['attrkey']) or {}
        values = data.get(self.__options['valuekey']) or ''
        return (attrs, values)

    def safedata(self, data, cdata=True):
        r"""Convert xml special chars to entities.

        :param data: the data will be converted safe.
        :param cdata: whether to use cdata. Default：``True``. If not, use :func:`cgi.escape` to convert data.
        :type cdata: bool
        :rtype: str
        """
        safe = ('<![CDATA[%s]]>' % data) if cdata else cgi.escape(str(data), True)
        return safe

    def build_tag(self, tag, text='', attrs=None):
        r"""Build tag full info include the attributes.

        :param tag: tag name.
        :param text: tag text.
        :param attrs: tag attributes. Default：``None``.
        :type attrs: dict or None
        :rtype: str
        """
        return '%s%s%s' % (self.tag_start(tag, attrs), text, self.tag_end(tag))

    def build_attr(self, attrs):
        r"""Build tag attributes.

        :param attrs: tag attributes
        :type attrs: dict
        :rtype: str
        """
        attrs = sorted(attrs.iteritems(), key=lambda x: x[0])
        return ' '.join(map(lambda x: '%s="%s"' % x, attrs))

    def tag_start(self, tag, attrs=None):
        r"""Build started tag info.

        :param tag: tag name
        :param attrs: tag attributes. Default：``None``.
        :type attrs: dict or None
        :rtype: str
        """
        return '<%s %s>' % (tag, self.build_attr(attrs)) if attrs else '<%s>' % tag

    def tag_end(self, tag):
        r"""Build closed tag info.

        :param tag: tag name
        :rtype: str
        """
        return '</%s>' % tag
