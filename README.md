lazyxml
=======


# 简介

简单的xml解析/生成库. 类似于simplejson的用法.


# 用法

- xml转换成python对象
```py
>>> import lazyxml
>>> xml = '<demo><foo>foo</foo><bar>bar</bar></demo>'
>>> lazyxml.loads(xml)
{'bar': 'bar', 'foo': 'foo'}
>>> lazyxml.loads(xml, strip_root=False)
{'demo': {'bar': 'bar', 'foo': 'foo'}}
>>> xml = '<demo><foo>foo</foo><bar>1</bar><bar>2</bar></demo>'
>>> lazyxml.loads(xml)
{'bar': ['1', '2'], 'foo': 'foo'}
```

- python对象转换成xml
```py
>>> data = {'demo':{'bar': ['1', '2'], 'foo': '<foo>'}}
>>> lazyxml.dumps(data)
'<?xml version="1.0" encoding="utf-8"?><demo><foo><![CDATA[<foo>]]></foo><bar><![CDATA[1]]></bar><bar><![CDATA[2]]></bar></demo>'
>>> lazyxml.dumps(data, cdata=False)
'<?xml version="1.0" encoding="utf-8"?><demo><foo>&lt;foo&gt;</foo><bar>1</bar><bar>2</bar></demo>'
>>> print lazyxml.dumps(data, indent='\t')
<?xml version="1.0" encoding="utf-8"?>
<demo>
	<foo><![CDATA[<foo>]]></foo>
	<bar><![CDATA[1]]></bar>
	<bar><![CDATA[2]]></bar>
</demo>
```

- 其他用法请见[demo](demo)
