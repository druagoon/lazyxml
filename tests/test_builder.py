# -*- coding: utf-8 -*-

#  MIT License
#
#  Copyright (c) 2019 Ryan Fau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

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
