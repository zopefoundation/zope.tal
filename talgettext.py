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
import string
import traceback

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



class POTALInterpreter(TALInterpreter):
    def translate(self, msgid, default, i18ndict=None, obj=None):
        # XXX is this right?
        if i18ndict is None:
            i18ndict = {}
        if obj:
            i18ndict.update(obj)
        # XXX Mmmh, it seems that sometimes the msgid is None; is that really
        # possible?
        if msgid is None:
            return None
        # XXX We need to pass in one of context or target_language
        return self.engine.translate(self.i18nContext.domain, msgid, i18ndict,
                                     position=self.position, default=default)


class POEngine(DummyEngine):
    __implements__ = ITALESEngine


    def __init__(self, macros=None):
        self.catalog = {}
        DummyEngine.__init__(self, macros)

    def evalaluate(*args):
        return '' # who cares

    def evaluatePathOrVar(*args):
        return '' # who cares

    def evaluateSequence(self, expr):
        return (0,) # dummy

    def evaluateBoolean(self, expr):
        return 1 # dummy

    def translate(self, domain, msgid, default, mapping, position):
        # assume domain and mapping are ignored; if they are not,
        # unit test must be updated.
        if msgid not in self.catalog:
            self.catalog[msgid] = []
            
        self.catalog[msgid].append((self.file, position))

        return 'x'

class UpdatePOEngine(POEngine):
    """A slightly-less braindead POEngine which supports loading an existing
    .po file first."""
    
    def __init__ (self, macros=None, filename=None):
        POEngine.__init__(self, macros)

        self._filename = filename
        self._loadFile()
        self.base = self.catalog
        self.catalog = {}

    def __add(self, id, str, fuzzy):
        "Add a non-fuzzy translation to the dictionary."
        if not fuzzy and str:
            # check for multi-line values and munge them appropriately
            if ('\n' in str):
                lines = str.rstrip().split('\n')
                str = string.join (lines, '"\n"')
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
            if not l.strip():
                continue
            # XXX: Does this always follow Python escape semantics?
            l = eval(l)
            if section == ID:
                msgid += l
            elif section == STR:
                msgstr += '%s\n' % l
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

    def translate(self, domain, msgid, mapping, position):
        if msgid not in self.base:
            POEngine.translate(self, domain, msgid, mapping, position)

        return 'x'
    
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
    update_mode = False
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-o', '--output'):
            outfile = arg
        elif opt in ('-u', '--update'):
            update_mode = True
            if outfile is None:
                outfile = arg
            engine = UpdatePOEngine(filename=arg)

    if not args:
        print 'nothing to do'
        return

    # We don't care about the rendered output of the .pt file
    class Devnull:
        def write(self, s):
            pass

    # check if we've already instantiated an engine;
    # if not, use the stupidest one available
    if not engine:
        engine = POEngine()

    # process each file specified
    for filename in args:
        try:
            engine.file = filename
            p = HTMLTALParser()
            p.parseFile(filename)
            program, macros = p.getCode()
            POTALInterpreter(program, macros, engine, stream=Devnull(),
                             metal=0)()
        except: # Hee hee, I love bare excepts!
            print 'There was an error processing', filename
            traceback.print_exc()

    # Now output the keys in the engine
    # write them to a file if --output is specified; otherwise use standard out
    if (outfile is None):
        outfile = sys.stdout
    else:
        outfile = file(outfile, update_mode and "a" or "w")
        
    msgids = engine.catalog.keys()
    msgids.sort()
    for msgid in msgids:
        positions = engine.catalog[msgid]
        for filename, position in positions:
            outfile.write('#: %s:%s\n' % (filename, position[0]))
            
        outfile.write('msgid "%s"\n' % msgid)
        outfile.write('msgstr ""\n')
        outfile.write('\n')

if __name__ == '__main__':
    main()
