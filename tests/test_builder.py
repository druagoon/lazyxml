# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import io
import unittest

import lazyxml


class BuilderTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BuilderTest, self).__init__(*args, **kwargs)
        self.data = {'demo': {'foo': '<foo>', 'bar': ['1', '2']}}
        self.xml = u'<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'

    def test_header_declare(self):
        b = u'<demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'
        self.assertEqual(lazyxml.dumps(self.data, header_declare=True), self.xml)
        self.assertEqual(lazyxml.dumps(self.data, header_declare=False), b)

    def test_cdata(self):
        b = u'<?xml version="1.0" encoding="utf-8"?><demo><foo>&lt;foo&gt;</foo><bar>1</bar><bar>2</bar></demo>'
        self.assertEqual(lazyxml.dumps(self.data, cdata=True), self.xml)
        self.assertEqual(lazyxml.dumps(self.data, cdata=False), b)

    def test_indent(self):
        b = u'<?xml version="1.0" encoding="utf-8"?>\n<demo>\n    <foo><![CDATA[<foo>]]></foo>\n    <bar><![CDATA[1]]></bar>\n    <bar><![CDATA[2]]></bar>\n</demo>'
        self.assertEqual(lazyxml.dumps(self.data), self.xml)
        self.assertEqual(lazyxml.dumps(self.data, indent=' ' * 4), b)

    def test_ksort(self):
        b = u'<?xml version="1.0" encoding="utf-8"?><demo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar><foo><![CDATA[<foo>]]></foo></demo>'
        self.assertEqual(lazyxml.dumps(self.data, ksort=False), self.xml)
        self.assertEqual(lazyxml.dumps(self.data, ksort=True), b)

    def test_dump_fileobj(self):
        buf = io.StringIO()
        lazyxml.dump(self.data, buf)
        self.assertEqual(buf.getvalue(), self.xml)
        buf.close()


if __name__ == '__main__':
    unittest.main()
