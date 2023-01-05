#!/usr/bin/env python
##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
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

from __future__ import print_function

import sys
import warnings

from zope.i18nmessageid import Message
from zope.interface import implementer

from zope.tal.dummyengine import DummyEngine
from zope.tal.interfaces import ITALExpressionEngine
from zope.tal.talinterpreter import TALInterpreter
from zope.tal.talinterpreter import normalize


PY3 = sys.version_info > (3,)
if PY3:
    unicode = str

pot_header = '''\
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR ORGANIZATION
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"POT-Creation-Date: %(time)s\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=CHARSET\\n"
"Content-Transfer-Encoding: ENCODING\\n"
"Generated-By: talgettext.py %(version)s\\n"
'''

NLSTR = '"\n"'


def usage(code, msg=''):
    # Python 2.1 required
    print(__doc__, file=sys.stderr)
    if msg:
        print(msg, file=sys.stderr)
    sys.exit(code)


class POTALInterpreter(TALInterpreter):
    def translate(self, msgid, default=None, i18ndict=None, obj=None):
        if default is None:
            default = getattr(msgid, 'default', unicode(msgid))
        # If no i18n dict exists yet, create one.
        if i18ndict is None:
            i18ndict = {}
        if obj:
            i18ndict.update(obj)
        # Mmmh, it seems that sometimes the msgid is None; is that really
        # possible?
        if msgid is None:
            return None
        # TODO: We need to pass in one of context or target_language
        return self.engine.translate(msgid, self.i18nContext.domain, i18ndict,
                                     default=default, position=self.position)


@implementer(ITALExpressionEngine)
class POEngine(DummyEngine):

    def __init__(self, macros=None):
        self.catalog = {}
        DummyEngine.__init__(self, macros)

    def evaluate(*args):
        # If the result of evaluate ever gets into a message ID, we want
        # to notice the fact in the .pot file.
        return '${DYNAMIC_CONTENT}'

    def evaluatePathOrVar(*args):
        # Actually this method is never called.
        return 'XXX'

    def evaluateSequence(self, expr):
        return (0,)  # dummy

    def evaluateBoolean(self, expr):
        return True  # dummy

    def translate(self, msgid, domain=None, mapping=None, default=None,
                  # Position is not part of the ITALExpressionEngine
                  # interface
                  position=None):

        if default is not None:
            default = normalize(default)
        if msgid == default:
            default = None
        msgid = Message(msgid, default=default)

        if domain not in self.catalog:
            self.catalog[domain] = {}
        domain = self.catalog[domain]

        if msgid not in domain:
            domain[msgid] = []
        else:
            msgids = list(domain)
            idx = msgids.index(msgid)
            existing_msgid = msgids[idx]
            if msgid.default != existing_msgid.default:
                references = '\n'.join([location[0] + ':' + str(location[1])
                                        for location in domain[msgid]])
                # Note: a lot of encode calls here are needed so
                # Python 3 does not break.
                warnings.warn(
                    "Warning: msgid '%s' in %s already exists "
                    "with a different default (bad: %s, should be: %s)\n"
                    "The references for the existent value are:\n%s\n" %
                    (msgid.encode('utf-8'),
                     self.file.encode('utf-8') + ':'.encode('utf-8')
                     + str(position).encode('utf-8'),
                     msgid.default.encode('utf-8'),
                     existing_msgid.default.encode('utf-8'),
                     references.encode('utf-8')))
        domain[msgid].append((self.file, position))
        return 'x'
