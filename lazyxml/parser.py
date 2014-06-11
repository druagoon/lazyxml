#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import utils


class Parser(object):
    r"""XML Parser
    """

    def __init__(self, **kw):
        self.__encoding = 'utf-8'           # 内部默认编码: utf-8

        self.__regex = {
            'xml_ns': re.compile(r'\{(.*?)\}(.*)'),  # XML命名空间正则匹配对象
            'xml_header': re.compile(r'<\?xml.*?\?>', re.I|re.S),  # XML头部声明正则匹配对象
            'xml_encoding': re.compile(r'<\?xml\s+.*?encoding="(.*?)".*?\?>', re.I|re.S)  # XML编码声明正则匹配对象
        }

        self.__options = {
            'encoding': None,               # XML编码
            'unescape': False,              # 是否转换HTML实体
            'strip_root': True,             # 是否去除根节点
            'strip': True,                  # 是否去除空白字符（换行符、制表符）
            'errors': 'strict',             # 解码错误句柄 参见: Codec Base Classes
        }

        self.set_options(**kw)

    def set_options(self, **kw):
        r"""Set Parser options.

        .. seealso::
            ``kw`` argument have the same meaning as in :func:`lazyxml.loads`
        """
        for k, v in kw.iteritems():
            if k in self.__options:
                self.__options[k] = v

    def get_options(self):
        r"""Get Parser options.
        """
        return self.__options

    def xml2dict(self, content):
        r"""Convert xml content to dict.

        .. warning::
            **DEPRECATED:** :meth:`xml2dict` is deprecated. Please use :meth:`xml2object` instead.

        .. deprecated:: 1.2
        """
        return self.xml2object(content)

    def xml2object(self, content):
        r"""Convert xml content to python object.

        :param content: xml content
        :rtype: dict

        .. versionadded:: 1.2
        """
        content = self.xml_filter(content)
        el = ET.fromstring(content)
        tree = self.parse(el)
        if not self.__options['strip_root']:
            node = self.get_node(el)
            return {node['tag']: tree}
        return tree

    def xml_filter(self, content):
        r"""Filter and preprocess xml content

        :param content: xml content
        :rtype: str
        """
        content = utils.strip_whitespace(content, True) if self.__options['strip'] else content.strip()

        if not self.__options['encoding']:
            encoding = self.guess_xml_encoding(content) or self.__encoding
            self.set_options(encoding=encoding)

        if self.__options['encoding'].lower() != self.__encoding:
            # 编码转换去除xml头
            content = self.strip_xml_header(content.decode(self.__options['encoding'], errors=self.__options['errors']))

        if self.__options['unescape']:
            content = utils.html_entity_decode(content)
        return content

    def guess_xml_encoding(self, content):
        r"""Guess encoding from xml header declaration.

        :param content: xml content
        :rtype: str or None
        """
        matchobj = self.__regex['xml_encoding'].match(content)
        return matchobj and matchobj.group(1).lower()

    def strip_xml_header(self, content):
        r"""Strip xml header

        :param content: xml content
        :rtype: str
        """
        return self.__regex['xml_header'].sub('', content)

    def parse(self, element):
        r"""Parse xml element.

        :param element: an :class:`~xml.etree.ElementTree.Element` instance
        :rtype: dict
        """
        values = {}
        for child in element:
            node = self.get_node(child)
            subs = self.parse(child)
            value = subs or node['value']
            if node['tag'] not in values:
                values[node['tag']] = value
            else:
                if not isinstance(values[node['tag']], list):
                    values[node['tag']] = [values.pop(node['tag'])]
                values[node['tag']].append(value)
        return values

    def get_node(self, element):
        r"""Parse element tag info.

        Parse element and get the element tag info. Include tag name, value, attribute, namespace.

        :param element: an :class:`~xml.etree.ElementTree.Element` instance
        :rtype: dict
        """
        ns, tag = self.split_namespace(element.tag)
        return {'tag': tag, 'value': (element.text or '').strip(), 'attr': element.attrib, 'namespace': ns}

    def split_namespace(self, tag):
        r"""Split tag namespace.

        :param tag: tag name
        :return: a pair of (namespace, tag)
        :rtype: tuple
        """
        matchobj = self.__regex['xml_ns'].search(tag)
        return matchobj.groups() if matchobj else ('', tag)
