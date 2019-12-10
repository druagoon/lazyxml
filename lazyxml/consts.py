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
