Changelog
=========


1.2.1 (2014-06-13)
------------------

- Python 2.5 or greater is required in version 1.2.1.
- Added ``strip_attr`` option to decide whether return the element attributes for parse result in :func:`lazyxml.loads` and :func:`lazyxml.load`.

1.2 (2014-06-10)
----------------

- `Sphinx <http://sphinx.pocoo.org/>`_ doc supported.
- The ``fp`` parameter for :func:`lazyxml.dump` is not just as a string of filename, also supports `file` or `file-like` object.
- :class:`collections.defaultdict` and :class:`collections.OrderedDict` supported in :func:`lazyxml.dump` and :func:`lazyxml.dumps`.
- :data:`types.GeneratorType` object and other iterable object that have `__iter__` and `next` attribute supported in :func:`lazyxml.dump` and :func:`lazyxml.dumps`.

1.1.0 (2014-05-06)
------------------

- First public version.

1.0.0 (2014-05-04)
------------------

- Move to github.
