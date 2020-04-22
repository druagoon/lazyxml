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

import html.entities

from .consts import Default, Regex


def html_entity_decode_char(matchobj, defs=html.entities.entitydefs):
    try:
        return defs[matchobj.group(1)]
    except KeyError:
        return matchobj.group(0)


def html_entity_decode(s):
    return Regex.HTML_ENTITY.sub(html_entity_decode_char, s)


def strip_whitespace(s, strict=False):
    s = s.replace('\r', '').replace('\n', '').replace('\t', '').replace('\x0B', '')
    return s.strip() if strict else s


def is_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True
