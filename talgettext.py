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
    -o / --output <file>
        Output the translation .po file to <file>.
    -u / --update <file>
        Update the existing translation <file> with any new translation strings
        found.
"""

import getopt
import os
import sys

from zope.tal.htmltalparser import HTMLTALParser
from zope.tal.talinterpreter import TALInterpreter
from zope.tal.dummyengine import DummyEngine
from zope.tal.interfaces import ITALESEngine
from zope.tal.taldefs import TALESError

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
        # assume domain and mapping are ignored; if they are not,
        # unit test must be updated.
        self.catalog[msgid] = ''

class UpdatePOEngine(POEngine):
    """A slightly-less braindead POEngine which supports loading an existing
    .po file first."""
    
    def __init__ (self, macros=None, filename=None):
        POEngine.__init__(self, macros)

        self._filename = filename
        self._loadFile()

    def __add(self, id, str, fuzzy):
        "Add a non-fuzzy translation to the dictionary."
        if not fuzzy and str:
            self.catalog[id] = str

    def _loadFile(self):
        # shamelessly cribbed from Python's Tools/i18n/msgfmt.py
        # Nathan R. Yergler (nathan@zope.org)
        # 25 March 2003
        
        ID = 1
        STR = 2

        try:
            lines = open(self._filename).readlines()
        except IOError, msg:
            print >> sys.stderr, msg
            sys.exit(1)

        section = None
        fuzzy = 0

        # Parse the catalog
        lno = 0
        for l in lines:
            lno += 1
            # If we get a comment line after a msgstr, this is a new entry
            if l[0] == '#' and section == STR:
                self.__add(msgid, msgstr, fuzzy)
                section = None
                fuzzy = 0
            # Record a fuzzy mark
            if l[:2] == '#,' and l.find('fuzzy'):
                fuzzy = 1
            # Skip comments
            if l[0] == '#':
                continue
            # Now we are in a msgid section, output previous section
            if l.startswith('msgid'):
                if section == STR:
                    self.__add(msgid, msgstr, fuzzy)
                section = ID
                l = l[5:]
                msgid = msgstr = ''
            # Now we are in a msgstr section
            elif l.startswith('msgstr'):
                section = STR
                l = l[6:]
            # Skip empty lines
            l = l.strip()
            if not l:
                continue
            # XXX: Does this always follow Python escape semantics?
            l = eval(l)
            if section == ID:
                msgid += l
            elif section == STR:
                msgstr += l
            else:
                print >> sys.stderr, 'Syntax error on %s:%d' % (infile, lno), \
                      'before:'
                print >> sys.stderr, l
                sys.exit(1)
        # Add last entry
        if section == STR:
            self.__add(msgid, msgstr, fuzzy)

    def evaluate(self, expression):
        try:
            return POEngine.evaluate(self, expression)
        except TALESError:
            pass
    
    def evaluatePathOrVar(self, expr):
        return 'who cares'

    def translate (self, domain, msgid, mapping):
        if (msgid not in self.catalog.keys()):
            self.catalog[msgid] = ''
    
def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            'ho:u:',
            ['help', 'output=', 'update='])
    except getopt.error, msg:
        usage(1, msg)

    outfile = None
    engine = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-o', '--output'):
            outfile = arg
        elif opt in ('-u', '--update'):
            engine = UpdatePOEngine(filename=arg)

    if not args:
        print 'nothing to do'
        return

    # We don't care about the rendered output of the .pt file
    class Devnull:
        def write(self, s):
            pass

    if not engine:
        engine = POEngine()
        
    for file in args:
        print file
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
