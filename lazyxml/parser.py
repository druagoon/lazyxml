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

import collections

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from . import utils
from .consts import Default, Regex


class Parser(object):
    """Simple xml parser
    """

    def __init__(self, encoding=None, unescape=False, strip_root=True,
                 strip_attr=True, strip=True, errors='strict'):
        """Constructor for Parser, with sensible defaults.

        :param str encoding: xml content encoding. if not set, will guess from xml header declare if possible.
        :param bool unescape: unescape xml html entity character. Default to ``False``.
        :param bool strip_root: strip root. Default to ``True``.
        :param bool strip_attr: strip tag attrs. Default to ``True``.
        :param bool strip: strip whitespace. Default to ``True``.
        :param string errors: xml content decode error handling scheme. Default to ``strict``.
        """
        self.__encoding = encoding
        self.__unescape = unescape
        self.__strip_root = strip_root
        self.__strip_attr = strip_attr
        self.__strip = strip
        self.__errors = errors

    def xml2dict(self, content):
        """Convert xml content to dict.

        .. warning::
            **DEPRECATED:** :meth:`xml2dict` is deprecated. Please use :meth:`xml2object` instead.

        .. deprecated:: 1.2
        """
        return self.xml2object(content)

    def xml2object(self, content):
        """Convert xml content to python object.

        :param content: xml content
        :rtype: dict

        .. versionadded:: 1.2
        """
        content = self.xml_filter(content)
        element = ET.fromstring(content)
        tree = self.parse(element) if self.__strip_attr else self.parse_full(element)
        if not self.__strip_root:
            node = self.get_node(element)
            if not self.__strip_attr:
                tree['attrs'] = node['attr']
            return {node['tag']: tree}
        return tree

    def xml_filter(self, content):
        """Filter and preprocess xml content

        :param content: xml content
        :rtype: str
        """
        content = utils.strip_whitespace(content, True) if self.__strip else content.strip()

        if not self.__encoding:
            self.__encoding = self.guess_xml_encoding(content) or Default.ENCODING
        if self.__encoding.lower() != Default.ENCODING:
            content = self.strip_xml_header(content.decode(self.__encoding, errors=self.__errors))
        if self.__unescape:
            content = utils.html_entity_decode(content)
        return content

    @staticmethod
    def guess_xml_encoding(content):
        """Guess encoding from xml header declaration.

        :param content: xml content
        :rtype: str or None
        """
        matchobj = Regex.XML_ENCODING.match(content)
        return matchobj and matchobj.group(1).lower()

    @staticmethod
    def strip_xml_header(content):
        """Strip xml header

        :param content: xml content
        :rtype: str
        """
        return Regex.XML_HEADER.sub('', content)

    @classmethod
    def parse(cls, element):
        """Parse xml element.

        :param element: an :class:`~xml.etree.ElementTree.Element` instance
        :rtype: dict
        """
        values = {}
        for child in element:
            node = cls.get_node(child)
            subs = cls.parse(child)
            value = subs or node['value']
            if node['tag'] not in values:
                values[node['tag']] = value
            else:
                if not isinstance(values[node['tag']], list):
                    values[node['tag']] = [values.pop(node['tag'])]
                values[node['tag']].append(value)
        return values

    @classmethod
    def parse_full(cls, element):
        """Parse xml element include the node attributes.

        :param element: an :class:`~xml.etree.ElementTree.Element` instance
        :rtype: dict

        .. versionadded:: 1.2.1
        """
        values = collections.defaultdict(dict)
        for child in element:
            node = cls.get_node(child)
            subs = cls.parse_full(child)
            value = subs or {'values': node['value']}
            value['attrs'] = node['attr']
            if node['tag'] not in values['values']:
                values['values'][node['tag']] = value
            else:
                if not isinstance(values['values'][node['tag']], list):
                    values['values'][node['tag']] = [values['values'].pop(node['tag'])]
                values['values'][node['tag']].append(value)
        return values

    @classmethod
    def get_node(cls, element):
        """Get node info.

        Parse element and get the element tag info. Include tag name, value, attribute, namespace.

        :param element: an :class:`~xml.etree.ElementTree.Element` instance
        :rtype: dict
        """
        ns, tag = cls.split_namespace(element.tag)
        return {
            'tag': tag,
            'value': (element.text or '').strip(),
            'attr': element.attrib,
            'namespace': ns
        }

    @staticmethod
    def split_namespace(tag):
        """Split tag namespace.

        :param tag: tag name
        :return: a pair of (namespace, tag)
        :rtype: tuple
        """
        matchobj = Regex.XML_NS.search(tag)
        return matchobj.groups() if matchobj else ('', tag)
