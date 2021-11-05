# -*- coding: utf-8 -*-

import re


class Default(object):
    VERSION = '1.0'
    ENCODING = 'utf-8'
    KEY_ATTR = '{attrs}'
    KEY_VALUE = '{values}'


class Regex(object):
    XML_NS = re.compile(r'\{(.*?)\}(.*)')  # XML Namespace
    XML_HEADER = re.compile(r'<\?xml.*?\?>', re.I | re.S)  # XML Header Declare
    XML_ENCODING = re.compile(r'<\?xml\s.*?encoding="(.*?)".*?\?>', re.I | re.S)  # XML Encoding
    HTML_ENTITY = re.compile('&(\w+?);')  # HTML Entity Character
