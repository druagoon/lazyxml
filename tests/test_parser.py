# -*- coding: utf-8 -*-

import sys
import io
import unittest
from collections import defaultdict

import lazyxml


class ParserTest(unittest.TestCase):

    def test_strip_root(self):
        xml = '<demo><foo>foo</foo><bar>1</bar><bar>2</bar></demo>'
        a = {'bar': ['1', '2'], 'foo': 'foo'}
        b = {'demo': {'bar': ['1', '2'], 'foo': 'foo'}}
        self.assertDictEqual(lazyxml.loads(xml), a)
        self.assertDictEqual(lazyxml.loads(xml, strip_root=False), b)

    def test_unescape(self):
        xml = '<root xmlns:h="http://www.w3.org/TR/html4/">&lt;demo&gt;&lt;foo&gt;foo&lt;/foo&gt;&lt;bar&gt;bar&lt;/bar&gt;&lt;/demo&gt;</root>'
        a = {'demo': {'bar': 'bar', 'foo': 'foo'}}
        b = {}
        self.assertDictEqual(lazyxml.loads(xml, unescape=True), a)
        self.assertDictEqual(lazyxml.loads(xml, unescape=False), b)

    def test_strip_attr(self):
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
        a = {
            'demo': defaultdict(dict, {
                'attrs': {'depth': '1', 'show': 'demo'},
                'values': {
                    'bar': [
                        {
                            'attrs': {
                                'depth': '2',
                                'show': 'bar-1'
                            },
                            'values': 'bar-1'
                        },
                        {
                            'attrs': {
                                'depth': '2',
                                'show': 'bar-2'
                            },
                            'values': 'bar-2'
                        }
                    ],
                    'foo': defaultdict(dict, {
                        'attrs': {
                            'depth': '2',
                            'show': 'foo'
                        },
                        'values': {
                            'subfoo': {
                                'attrs': {
                                    'depth': '3',
                                    'show': 'subfoo'
                                },
                                'values': 'subfoo'
                            }
                        }
                    })
                }
            })
        }
        b = {'demo': {'bar': ['bar-1', 'bar-2'], 'foo': {'subfoo': 'subfoo'}}}
        self.assertEqual(lazyxml.loads(xml, strip_root=False, strip_attr=False),
                         a)
        self.assertEqual(lazyxml.loads(xml, strip_root=False, strip_attr=True),
                         b)

    def test_encoding(self):
        xml = """
        <?xml version="1.0" encoding="gbk"?>
        <string xmlns="http://www.w3.org/TR/html4/">
            <Response>
                <Result>true</Result>
                <Reason>保存成功</Reason>
            </Response>
        </string>
        """
        a = {
            'Response': {
                'Reason': '\u4fdd\u5b58\u6210\u529f',
                'Result': 'true'
            }
        }
        self.assertDictEqual(lazyxml.loads(xml), a)

    def test_namespace(self):
        xml = """
        <?xml version="1.0" encoding="UTF-8"?>
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
            <xsl:template match="/">
                <html>
                    <body>
                        <h2>My CD Collection</h2>
                        <table border="1">
                            <tr>
                                <th align="left">Title</th>
                                <th align="left">Artist</th>
                            </tr>
                            <xsl:for-each select="catalog/cd">
                                <tr>
                                    <td>
                                        <xsl:value-of select="title"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="artist"/>
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </table>
                    </body>
                </html>
            </xsl:template>
        </xsl:stylesheet>
        """
        a = {
            'template': {
                'html': {
                    'body': {
                        'h2': 'My CD Collection',
                        'table': {
                            'for-each': {
                                'tr': {
                                    'td': [{'value-of': ''}, {'value-of': ''}]
                                }
                            },
                            'tr': {'th': ['Title', 'Artist']}
                        }
                    }
                }
            }
        }
        self.assertDictEqual(lazyxml.loads(xml), a)

    def test_load_fileobj(self):
        xml = '<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'
        buf = io.StringIO(xml)
        a = {'bar': ['1', '2'], 'foo': '<foo>'}
        self.assertDictEqual(lazyxml.load(buf), a)
        buf.close()


if __name__ == '__main__':
    unittest.main()
