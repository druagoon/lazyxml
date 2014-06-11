#!/usr/bin/env python
# -*- coding: utf-8 -*-


r"""The common tools
"""

import re
import sys
import types
import collections
import htmlentitydefs


HTML_ENTITY_PATTERN = re.compile('&(\w+?);')

DictTypes = [dict]
if sys.version_info >= (2, 5):
    DictTypes.append(collections.defaultdict)
if sys.version_info >= (2, 7):
    DictTypes.append(collections.OrderedDict)
DictTypes = tuple(DictTypes)


def html_entity_decode_char(matchobj, defs=htmlentitydefs.entitydefs):
    try:
        return defs[matchobj.group(1)]
    except KeyError:
        return matchobj.group(0)


def html_entity_decode(s):
    return HTML_ENTITY_PATTERN.sub(html_entity_decode_char, s)


def strip_whitespace(s, strict=False):
    s = s.replace('\r', '').replace('\n', '').replace('\t', '').replace('\x0B', '')
    return s.strip() if strict else s


def is_iterable(obj):
    return isinstance(obj, (list, tuple, types.GeneratorType)) \
        or all(map(lambda attr: hasattr(obj, attr), ['__iter__', 'next']))

