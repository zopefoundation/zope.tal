##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Tests that run driver.py over input files comparing to output files.
"""

import glob
import os
import sys
import unittest

try:
    # Python 2.x
    from cStringIO import StringIO
except ImportError:
    # Python 3.x
    from io import StringIO

import zope.tal.runtest

from zope.tal.tests import utils

HERE = os.path.abspath(os.path.dirname(__file__))
PARENTDIR = os.path.dirname(HERE)
PREFIX = os.path.join(HERE, "input", "test*.")


def _factory(filename, dirname):

    old_stdout = sys.stdout
    pwd = os.getcwd()
    short_path = os.path.relpath(filename, os.path.dirname(__file__))

    def setUp():
        os.chdir(dirname)
        sys.stdout = StringIO()

    def tearDown():
        os.chdir(pwd)
        sys.stdout = old_stdout

    def runTest():
        basename = os.path.basename(filename)
        if basename.startswith('test_sa'):
            sys.argv = ["runtest.py", "-Q", "-a", filename]
        elif basename.startswith('test_metal'):
            sys.argv = ["runtest.py", "-Q", "-m", filename]
        else:
            sys.argv = ["runtest.py", "-Q", filename]
        try:
            failed = zope.tal.runtest.main()
        finally:
            captured_stdout = sys.stdout.getvalue()
        if failed:
            raise AssertionError("output for %s didn't match:\n%s"
                                    % (filename, captured_stdout))

    return unittest.FunctionTestCase(runTest, setUp, tearDown, short_path)


def _find_files():
    if utils.skipxml:
        xmlargs = []
    else:
        xmlargs = sorted(glob.glob(PREFIX + "xml"))
    htmlargs = sorted(glob.glob(PREFIX + "html"))

    args = xmlargs + htmlargs
    if not args:
        sys.stderr.write("Warning: no test input files found!!!\n")
    return args

# Nose doesn't handle 'test_suite' in the same was as zope.testrunner,
# so we'll use its generator-as-test-factory feature.  See:
# https://nose.readthedocs.org/en/latest/writing_tests.html#test-generators
def test_for_nose_discovery():
    for arg in _find_files():
        yield _factory(arg, PARENTDIR)

def test_suite():
    return unittest.TestSuite(
        [_factory(arg, PARENTDIR) for arg in _find_files()])
