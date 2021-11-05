# -*- coding: utf-8 -*-

import sys

from setuptools import setup

import lazyxml

if sys.version_info[:2] < (2, 7) or sys.version_info[0] >= 3:
    sys.exit('Python 2.7.x is required.')

with open('README.md') as fp:
    readme = fp.read()

setup(name=lazyxml.__title__,
      version=lazyxml.__version__,
      description=lazyxml.__description__,
      long_description_content_type='text/markdown',
      long_description=readme,
      author=lazyxml.__author__,
      author_email=lazyxml.__author_email__,
      maintainer=lazyxml.__author__,
      maintainer_email=lazyxml.__author_email__,
      url='https://github.com/druagoon/lazyxml',
      packages=[lazyxml.__title__],
      license=lazyxml.__license__,
      python_requires='>=2.7, <3.0',
      classifiers=[]
      )
