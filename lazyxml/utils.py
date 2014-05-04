#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import htmlentitydefs


html_entity_pattern = re.compile("&(\w+?);")

def html_entity_decode_char(m, defs=htmlentitydefs.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)


def html_entity_decode(s):
    return html_entity_pattern.sub(html_entity_decode_char, s)


def strip_whitespace(s, strict=False):
    s = s.replace('\r', '').replace('\n', '').replace('\t', '').replace('\x0B', '')
    return s.strip() if strict else s
