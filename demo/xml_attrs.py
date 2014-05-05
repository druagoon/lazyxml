#!/usr/bin/env python
# -*- coding: utf-8 -*-

import compat
import lazyxml


attr_key = 'attr'
value_key = 'value'

demo = {
    'root': {
        value_key: {
            'a': {
                attr_key:{
                    'a1': 'a1'
                },
                value_key: {
                    'sku': '2',
                    'num': 1
                }
            },
            'b': {
                attr_key:{
                    'b1': 'b1'
                },
                value_key: '版本'
            },
            'c': {
                attr_key:{
                    'c1': 'c1'
                },
                value_key: {
                    'c_items': [
                        {
                        'sku': '2',
                        'num': 1
                        },
                        {
                        'sku': '2',
                        'num': 1
                        }
                    ]
                }
            },
            'd': {
                attr_key:{
                    'd1': 'd1'
                },
                value_key: {
                    'd11': {
                        attr_key: {
                            'd11': 'd11'
                        },
                        value_key: {
                            'sku_d': 1,
                            'num_d': 12,
                            'child_1': {
                                'q1': 'q1',
                                'q2': 2,
                                'q3': '34'
                            }
                        }
                    }
                }
            },
            'e': '',
            'f': {
                attr_key:{
                    'f1': 'f1'
                },
            },
            'g': [
                {
                    'g1': '&&g1',
                },
                {
                    'g2': '&&g2',
                }
            ],
            # h will be empty
            'h': {
                'h1': 'h1',
                'h2': '<h2>',
            }
        }
    }
}

if __name__ == '__main__':
    kw = {
        'hasattr': True,
        'indent': '\t',
        'cdata': False
    }
    print lazyxml.dumps(demo, **kw)
    lazyxml.dump(demo, 'dump.xml', **kw)
