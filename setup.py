##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.tal package

$Id$
"""
import os
import sys
from setuptools import setup, find_packages

here = os.path.dirname(__file__)

def read(*rnames):
    return open(os.path.join(here, *rnames)).read()

def alltests():
    # use the zope.testing testrunner machinery to find all the
    # test suites we've put under ourselves
    from zope.testing.testrunner import get_options
    from zope.testing.testrunner import find_suites
    from zope.testing.testrunner import configure_logging
    configure_logging()
    from unittest import TestSuite
    here = os.path.abspath(os.path.dirname(sys.argv[0]))
    args = sys.argv[:]
    src = os.path.join(here, 'src')
    defaults = ['--test-path', src]
    options = get_options(args, defaults)
    suites = list(find_suites(options))
    return TestSuite(suites)

setup(name='zope.tal',
      version = '3.5.2',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Zope 3 Template Application Languate (TAL)',
      long_description=(
          read('README.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope3 template xml tal",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/zope.tal',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope'],
      extras_require = dict(
          test=['zope.testing',
                ]),
      test_suite="__main__.alltests", # to support "setup.py test"
      tests_require = ['zope.testing'],
      install_requires=['setuptools',
                        'zope.i18nmessageid',
                        'zope.interface',
                       ],
      include_package_data = True,
      zip_safe = False,
      )
