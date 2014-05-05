#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import with_statement

import compat
import lazyxml


def main(filename='unescape.xml'):
    with open(filename, 'rb') as fp:
        print lazyxml.load(fp, unescape=True)


if __name__ == '__main__':
    main()
