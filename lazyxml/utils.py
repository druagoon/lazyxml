# -*- coding: utf-8 -*-

import htmlentitydefs

from .consts import Default, Regex


def html_entity_decode_char(matchobj, defs=htmlentitydefs.entitydefs):
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
