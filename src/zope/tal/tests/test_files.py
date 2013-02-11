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


class FileTestCase(unittest.TestCase):

    def __init__(self, file, dir):
        self.__file = file
        self.__dir = dir
        unittest.TestCase.__init__(self)

    # For unittest.
    def shortDescription(self):
        path = os.path.basename(self.__file)
        return '%s (%s)' % (path, self.__class__)

    def id(self):
        return os.path.relpath(self.__file, os.path.dirname(__file__))

    __str__ = id

    def runTest(self):
        basename = os.path.basename(self.__file)
        if basename.startswith('test_sa'):
            sys.argv = ["runtest.py", "-Q", "-a", self.__file]
        elif basename.startswith('test_metal'):
            sys.argv = ["runtest.py", "-Q", "-m", self.__file]
        else:
            sys.argv = ["runtest.py", "-Q", self.__file]
        pwd = os.getcwd()
        try:
            os.chdir(self.__dir)
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            failed = zope.tal.runtest.main()
        finally:
            captured_stdout = sys.stdout.getvalue()
            sys.stdout = old_stdout
            os.chdir(pwd)
        if failed:
            self.fail("output for %s didn't match:\n%s"
                      % (self.__file, captured_stdout))

try:
    script = __file__
except NameError:
    script = sys.argv[0]

def test_suite():
    suite = unittest.TestSuite()
    dir = os.path.dirname(script)
    dir = os.path.abspath(dir)
    parentdir = os.path.dirname(dir)
    prefix = os.path.join(dir, "input", "test*.")
    if utils.skipxml:
        xmlargs = []
    else:
        xmlargs = glob.glob(prefix + "xml")
        xmlargs.sort()
    htmlargs = glob.glob(prefix + "html")
    htmlargs.sort()
    args = xmlargs + htmlargs
    if not args:
        sys.stderr.write("Warning: no test input files found!!!\n")
    for arg in args:
        case = FileTestCase(arg, parentdir)
        suite.addTest(case)
    return suite

if __name__ == "__main__":
    errs = utils.run_suite(test_suite())
    sys.exit(errs and 1 or 0)
