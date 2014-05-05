#!/usr/bin/env python
# -*- coding: utf-8 -*-


import compat
import lazyxml

s = {
    'notify_id'         :   '1111111111111111111111',
    'custom_id'         :   '1356765333',
    'out_order_code'    :   '111111111',
    'warehouse_code'    :   'KU-004',
    'logistics_code'    :   'STO',
    'logistics_name'    :   '',
    'logistics_no'      :   '2222222',
    'weight'            :   2.3,
    'volume'            :   3,
    'status_code'       :   'WMS_PACKAGE',
    'status_info'       :   '已打包',
    'remark'            :   '<备注>',
    'create_time'       :   '2011-08-12 17:36:24',
    'items'             :   {
        'item'      :       [
            {
                'item_line_num'     :   1,
                'item_code'         :   '123456',
                'good_num'          :   5,
                'bad_num'           :   0,
            },
            {
                'item_line_num'     :   1,
                'item_code'         :   '123456',
                'good_num'          :   5,
                'bad_num'           :   0,
            }
        ]
    }
}

if __name__ == '__main__':
    filename = 'dump.xml'
    kw = {
        'root': 'notify',
        'indent': '\t',
        'encoding': 'gbk'
    }
    print lazyxml.dumps(s, **kw)
    lazyxml.dump(s, filename, **kw)
