# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.insert(0, os.path.abspath('../'))

import lazyxml


def main():
    xml = '<demo><foo>foo</foo><bar>1</bar><bar>2</bar></demo>'

    # 默认
    print lazyxml.loads(xml)

    # 去除根节点
    print lazyxml.loads(xml, strip_root=False)

    xml = """
    <demo depth="1" show="demo">
        <foo depth="2" show="foo">
            <subfoo depth="3" show="subfoo">
                subfoo
            </subfoo>
        </foo>
        <bar depth="2" show="bar-1">bar-1</bar>
        <bar depth="2" show="bar-2">bar-2</bar>
    </demo>
    """
    print lazyxml.loads(xml, strip_root=False, strip_attr=False)

    # html实体字符转换
    xml = '<root xmlns:h="http://www.w3.org/TR/html4/">&lt;demo&gt;&lt;foo&gt;foo&lt;/foo&gt;&lt;bar&gt;bar&lt;/bar&gt;&lt;/demo&gt;</root>'
    print lazyxml.loads(xml, unescape=True)

    # 自动猜测编码 也可以手动执行编码
    with open('xml/gbk.xml', 'rb') as fp:
        xml = fp.read()
        print lazyxml.loads(xml)

    # 从文件句柄加载xml 命名空间会自动过滤
    with open('xml/namespace.xml', 'rb') as fp:
        print lazyxml.load(fp)

    # 从类文件对象加载xml
    from cStringIO import StringIO

    buffer = StringIO(
        '<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>')
    print lazyxml.load(buffer)
    buffer.close()


if __name__ == '__main__':
    main()
