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
"""Tests for TALInterpreter."""

import sys
import unittest

from StringIO import StringIO

from zope.tal.taldefs import METALError, I18NError
from zope.tal.htmltalparser import HTMLTALParser
from zope.tal.talinterpreter import TALInterpreter
from zope.tal.dummyengine import DummyEngine
from zope.tal.tests import utils


class TestCaseBase(unittest.TestCase):

    def _compile(self, source):
        parser = HTMLTALParser()
        parser.parseString(source)
        program, macros = parser.getCode()
        return program, macros


class MacroErrorsTestCase(TestCaseBase):

    def setUp(self):
        dummy, macros = self._compile('<p metal:define-macro="M">Booh</p>')
        self.macro = macros['M']
        self.engine = DummyEngine(macros)
        program, dummy = self._compile('<p metal:use-macro="M">Bah</p>')
        self.interpreter = TALInterpreter(program, {}, self.engine)

    def tearDown(self):
        try:
            self.interpreter()
        except METALError:
            pass
        else:
            self.fail("Expected METALError")

    def test_mode_error(self):
        self.macro[1] = ("mode", "duh")

    def test_version_error(self):
        self.macro[0] = ("version", "duh")


class I18NErrorsTestCase(TestCaseBase):

    def _check(self, src, msg):
        try:
            self._compile(src)
        except I18NError:
            pass
        else:
            self.fail(msg)

    def test_id_with_replace(self):
        self._check('<p i18n:id="foo" tal:replace="string:splat"></p>',
                    "expected i18n:id with tal:replace to be denied")

    def test_missing_values(self):
        self._check('<p i18n:attributes=""></p>',
                    "missing i18n:attributes value not caught")
        self._check('<p i18n:data=""></p>',
                    "missing i18n:data value not caught")
        self._check('<p i18n:id=""></p>',
                    "missing i18n:id value not caught")

    def test_id_with_attributes(self):
        self._check('''<input name="Delete"
                       tal:attributes="name string:delete_button"
                       i18n:attributes="name message-id">''',
            "expected attribute being both part of tal:attributes" +
            " and having a msgid in i18n:attributes to be denied")

class OutputPresentationTestCase(TestCaseBase):

    def test_attribute_wrapping(self):
        # To make sure the attribute-wrapping code is invoked, we have to
        # include at least one TAL/METAL attribute to avoid having the start
        # tag optimized into a rawtext instruction.
        INPUT = r"""
        <html this='element' has='a' lot='of' attributes=', so' the='output'
              needs='to' be='line' wrapped='.' tal:define='foo nothing'>
        </html>"""
        EXPECTED = r'''
        <html this="element" has="a" lot="of"
              attributes=", so" the="output" needs="to"
              be="line" wrapped=".">
        </html>''' "\n"
        self.compare(INPUT, EXPECTED)

    def test_entities(self):
        INPUT = ('<img tal:define="foo nothing" '
                 'alt="&a; &#1; &#x0a; &a &#45 &; &#0a; <>" />')
        EXPECTED = ('<img alt="&a; &#1; &#x0a; '
                    '&amp;a &amp;#45 &amp;; &amp;#0a; &lt;&gt;" />\n')
        self.compare(INPUT, EXPECTED)

    def compare(self, INPUT, EXPECTED):
        program, macros = self._compile(INPUT)
        sio = StringIO()
        interp = TALInterpreter(program, {}, DummyEngine(), sio, wrap=60)
        interp()
        self.assertEqual(sio.getvalue(), EXPECTED)


def test_suite():
    suite = unittest.makeSuite(I18NErrorsTestCase)
    suite.addTest(unittest.makeSuite(MacroErrorsTestCase))
    suite.addTest(unittest.makeSuite(OutputPresentationTestCase))
    return suite

if __name__ == "__main__":
    errs = utils.run_suite(test_suite())
    sys.exit(errs and 1 or 0)
