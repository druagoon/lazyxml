# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.insert(0, os.path.abspath('../'))

import lazyxml

ATTRKEY = '{{attrs}}'
VALUEKEY = '{{values}}'

ATTRDATA = {
    'root': {
        ATTRKEY: {'a1': 1, 'a2': 2},
        VALUEKEY: {
            'test1': {
                ATTRKEY: {'b': 2, 'a': 1, 'c': 3},
                VALUEKEY: {
                    # 重复方式-1: 所有的重复使用相同的属性(子节点重复)
                    'repeat1': {
                        ATTRKEY: {'required': 'false', 'index': 1},
                        VALUEKEY: [{'foo': '<foo-1>', 'bar': ['1', '2']}, {'foo': '<foo-2>', 'bar': ['3', '4']}]
                    },
                    # 重复方式-2: 所有的重复使用相同的属性(当前节点重复)
                    'repeat2': {
                        ATTRKEY: {'required': 'true', 'index': '2'},
                        VALUEKEY: [1, 2]
                    },
                    # 重复方式-3: 同一个节点使用不同的属性
                    'repeat3': [
                        {
                            ATTRKEY: {'required': 'true', 'index': '3'},
                            VALUEKEY: {'sub': [1, 2]}
                        },
                        {
                            ATTRKEY: {'required': 'true', 'index': '4'},
                            VALUEKEY: {'sub': [1, 2, 3]}
                        },
                    ],
                    'normal': {
                        ATTRKEY: {'required': 'false', 'index': 5},
                        VALUEKEY: {'foo': '<foo-1>', 'bar': ['1', '2']}
                    }
                }
            },
            'test2': {
                ATTRKEY: {'b': 2, 'a': 1, 'c': 3},
                VALUEKEY: u'测试用'
            }
        }
    }
}


def main():
    data = {'demo':{'foo': '<foo>', 'bar': ['1', '2']}}

    # xml写入文件 提供文件名
    lazyxml.dump(data, 'xml/dump.xml')

    # xml写入文件 提供文件句柄
    with open('xml/dump-fp.xml', 'w') as fp:
        lazyxml.dump(data, fp)

    # xml写入文件 提供类文件对象
    from cStringIO import StringIO
    buffer = StringIO()
    lazyxml.dump(data, buffer)
    print buffer.getvalue()
    # <?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[1]]></foo><bar><![CDATA[2]]></bar></demo>
    buffer.close()

    # 默认
    print lazyxml.dumps(data)
    # '<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'

    # 不声明xml头部
    print lazyxml.dumps(data, header_declare=False)
    # '<demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'

    # 不使用CDATA格式
    print lazyxml.dumps(data, cdata=False)
    # '<?xml version="1.0" encoding="utf-8"?><demo><foo>&lt;foo&gt;</foo><bar>1</bar><bar>2</bar></demo>'

    # 缩进和美观xml
    print lazyxml.dumps(data, indent=' ' * 4)
    # <?xml version="1.0" encoding="utf-8"?>
    # <demo>
    #     <foo><![CDATA[<foo>]]></foo>
    #     <bar><![CDATA[1]]></bar>
    #     <bar><![CDATA[2]]></bar>
    # </demo>

    # 使用标签名称排序
    print lazyxml.dumps(data, ksort=True)
    # '<?xml version="1.0" encoding="utf-8"?><demo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar><foo><![CDATA[<foo>]]></foo></demo>'

    # 使用标签名称倒序排序
    print lazyxml.dumps(data, ksort=True, reverse=True)
    # '<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'

    # 含有属性的xml数据
    kw = {
        'hasattr': True,
        'ksort': True,
        'indent': ' ' * 4,
        'attrkey': ATTRKEY,
        'valuekey': VALUEKEY
    }
    print lazyxml.dumps(ATTRDATA, **kw)
    """
    <root a1="1" a2="2">
        <test1 a="1" b="2" c="3">
            <normal index="5" required="false">
                <bar><![CDATA[1]]></bar>
                <bar><![CDATA[2]]></bar>
                <foo><![CDATA[<foo-1>]]></foo>
            </normal>
            <repeat1 index="1" required="false">
                <bar><![CDATA[1]]></bar>
                <bar><![CDATA[2]]></bar>
                <foo><![CDATA[<foo-1>]]></foo>
            </repeat1>
            <repeat1 index="1" required="false">
                <bar><![CDATA[3]]></bar>
                <bar><![CDATA[4]]></bar>
                <foo><![CDATA[<foo-2>]]></foo>
            </repeat1>
            <repeat2 index="2" required="true"><![CDATA[1]]></repeat2>
            <repeat2 index="2" required="true"><![CDATA[2]]></repeat2>
            <repeat3 index="3" required="true">
                <sub><![CDATA[1]]></sub>
                <sub><![CDATA[2]]></sub>
            </repeat3>
            <repeat3 index="4" required="true">
                <sub><![CDATA[1]]></sub>
                <sub><![CDATA[2]]></sub>
                <sub><![CDATA[3]]></sub>
            </repeat3>
        </test1>
        <test2 a="1" b="2" c="3"><![CDATA[测试用]]></test2>
    </root>
    """

if __name__ == '__main__':
    main()
