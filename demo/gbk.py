#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import with_statement

import compat
import lazyxml


def main(filename='gbk.xml'):
    with open(filename, 'rb') as fp:
        xml = fp.read()
    print lazyxml.loads(xml, strip_root=False)


if __name__ == '__main__':
    main()
