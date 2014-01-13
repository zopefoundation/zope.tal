=======
CHANGES
=======

4.0.0a2 (unreleased)
--------------------

- Fix possible UnicodeDecodeError in warning when msgid already exists.


4.0.0a1 (2013-02-15)
--------------------

- Replaced deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Dropped support for Python 2.4 and 2.5.

- Experimental Python 3.3 and PyPy support (all tests pass, but test
  coverage is not complete).

- Output generated attributes (via tal:attributes and i18n:attributes
  directives) in alphabetical order.


3.6.1 (2012-03-09)
------------------

- Avoid handling end tags within <script> tags in the HTML parser. This works
  around http://bugs.python.org/issue670664

- Fixed documentation link in README.txt.

3.6.0 (2011-08-20)
------------------

- Updated `talinterpreter.FasterStringIO` to faster list-based implementation.

- Increase the default value of the `wrap` argument from 60 to 1023 characters,
  to avoid extra whitespace and line breaks.

- Fix printing of error messages for msgid conflict with non-ASCII texts.


3.5.2 (2009-10-31)
------------------

- In talgettext.POEngine.translate, print a warning if a msgid already exists
  in the domain with a different default.


3.5.1 (2009-03-08)
------------------

- Updated tests of "bad" entities for compatibility with the stricter
  HTMLParser module shipped with Python 2.6.x.


3.5.0 (2008-06-06)
------------------

- Removed artificial addition of a trailing newline if the output doesn't end
  in one; this allows the template source to be the full specification of what
  should be included.
  (See https://bugs.launchpad.net/launchpad/+bug/218706.)


3.4.1 (2007-11-16)
------------------

- Removed unnecessary ``dummyengine`` dependency on zope.i18n to
  simplify distribution.  The ``dummyengine.DummyTranslationDomain``
  class no longer implements
  ``zope.i18n.interfaces.ITranslationDomain`` as a result.  Installing
  zope.tal with easy_install or buildout no longer pulls in many
  unrelated distributions.

- Support ability to run tests using "setup.py test".

- Stop pinning (no longer required) zope.traversing and
  zope.app.publisher versions in buildout.cfg.


3.4.0 (2007-10-03)
------------------

- Updated package meta-data.


3.4.0b1
-------

- Updated dependency for ``zope.i18n`` that requires the correct version of
  zope.security to avoid a hidden dependency issue in zope.security.

Note: The code changes before 3.4.0b1 where not tracked as an individual
package and have been documented in the Zope 3 changelog.
