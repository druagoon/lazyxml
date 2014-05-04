#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import utils


class Parser(object):
    """
    XML Parser
    """

    def __init__(self, **kw):
        self.__encoding = 'utf-8'  # 内部默认编码: utf-8

        self.__regex = {
            'xml_ns': re.compile(r"\{(.*)\}(.*)"),  # XML命名空间正则匹配对象
            'xml_header': re.compile(r'<\?xml\s+[^>]*\?>', re.I)  # XML头部正则匹配对象 不区分大小写
        }

        # 默认参数选项
        self.__options = {
            'encoding': 'utf-8',            # XML编码
            'unescape': False,              # 是否转换HTML实体
            'strip_root': True,             # 是否去除解析根节点
            'strip': True                   # 是否去除空白字符
        }

        self.set_options(**kw)

    def set_options(self, **kw):
        for k, v in kw.iteritems():
            if k in self.__options:
                self.__options[k] = v

    def get_options(self):
        return self.__options

    def xml2dict(self, content):
        """
        # xml content to dict object
        # @param   str content
        # @return  dict
        # @todo
        """
        content = self.xml_filter(content)
        el = ET.fromstring(content)
        tree = self.parse(el)
        return tree if self.__options['strip_root'] else {el.tag: tree}

    def xml_filter(self, content):
        """
        # 解析xml前过一些过滤和转换 使xml可解析
        """
        content = utils.strip_whitespace(content, True) if self.__options['strip'] else content.strip()
        if self.__options['encoding'].lower() != self.__encoding:
            content = self.strip_xml_header(content.decode(self.__options['encoding'], 'xmlcharrefreplace'))  # 非内部utf-8编码需作编码转换并去除xml头部
        if self.__options['unescape']:
            content = utils.html_entity_decode(content)
        return content

    def strip_xml_header(self, content):
        return self.__regex['xml_header'].sub('', content)

    def parse(self, element):
        """
        # parse element
        # @param   object[Element] el
        # @return  dict
        # @todo
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

    def get_node(self, el):
        """
        # parse element tag info
        # @param   object[Element] el
        # @return  dict
        # @todo
        """
        ns, tag = self.split_namespace(el.tag)
        return {'tag': tag, 'value': (el.text or '').strip(), 'attr': el.attrib, 'namespace': ns}

    def split_namespace(self, tag):
        """
        # parse tag namespace
        # @param   str tag
        # @return  tuple (namespace, tag)
        # @todo
        """
        result = self.__regex['xml_ns'].search(tag)
        return result.groups() if result else ('', tag)
