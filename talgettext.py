#!/usr/bin/env python
##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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

"""Program to extract internationalization markup from Page Templates.

Once you have marked up a Page Template file with i18n: namespace tags, use
this program to extract GNU gettext .po file entries.

Usage: talgettext.py [options] files
Options:
    -h / --help
        Print this message and exit.
"""

import getopt
import os
import sys

from zope.tal.htmltalparser import HTMLTALParser
from zope.tal.talinterpreter import TALInterpreter
from zope.tal.dummyengine import DummyEngine
from zope.tal.interfaces import ITALESEngine


def usage(code, msg=''):
    # Python 2.1 required
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)


class POEngine(DummyEngine):
    __implements__ = ITALESEngine

    catalog = {}

    def evaluatePathOrVar(self, expr):
        return 'who cares'

    def translate(self, domain, msgid, mapping):
        self.catalog[msgid] = ''


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            'ho:',
            ['help', 'output='])
    except getopt.error, msg:
        usage(1, msg)

    outfile = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-o', '--output'):
            outfile = arg

    if not args:
        print 'nothing to do'
        return

    # We don't care about the rendered output of the .pt file
    class Devnull:
        def write(self, s):
            pass

    engine = POEngine()
    for file in args:
        p = HTMLTALParser()
        p.parseFile(file)
        program, macros = p.getCode()
        TALInterpreter(program, macros, engine, stream=Devnull())()

    # Now print all the entries in the engine
    msgids = engine.catalog.keys()
    msgids.sort()
    for msgid in msgids:
        msgstr = engine.catalog[msgid]
        print 'msgid "%s"' % msgid
        print 'msgstr "%s"' % msgstr
        print


if __name__ == '__main__':
    main()
