#! /usr/bin/env python
##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Run all tests."""

import sys
import unittest

import zope.tal.tests.utils
import zope.tal.tests.test_htmltalparser
import zope.tal.tests.test_talinterpreter
import zope.tal.tests.test_files
import zope.tal.tests.test_sourcepos

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(test_htmltalparser.test_suite())
    if not utils.skipxml:
        import test_xmlparser
        suite.addTest(test_xmlparser.test_suite())
    suite.addTest(test_talinterpreter.test_suite())
    suite.addTest(test_files.test_suite())
    suite.addTest(test_sourcepos.test_suite())
    return suite

def main():
    return utils.run_suite(test_suite())

if __name__ == "__main__":
    errs = main()
    sys.exit(errs and 1 or 0)
