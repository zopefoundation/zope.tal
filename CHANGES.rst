=========
 Changes
=========

6.0 (2025-09-12)
================

- Replace ``pkg_resources`` namespace with PEP 420 native namespace.


5.1.1 (2025-08-14)
==================

- Fix tests for Python 3.13.6+ compatibility.


5.1 (2025-02-14)
================

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7, 3.8.


5.0.1 (2023-01-23)
==================

- Add missing ``python_requires`` to ``setup.py``.


5.0 (2023-01-19)
================

- Add support for Python 3.11.

- Drop support for Python 2.7, 3.5, 3.6.

- Add support for Python 3.10.

- Add ``nav`` to the list of HTML block level elements.
  (`#18 <https://github.com/zopefoundation/zope.tal/pull/18>`_)

- Remove ``.talgettext.UpdatePOEngine`` and the ability to call
  ``zope/tal/talgettext.py`` (main function). The code was broken and unused.

- Remove support to run the tests using deprecated ``python setup.py test``.


4.5 (2021-05-28)
================

- Avoid traceback reference cycle in ``TALInterpreter.do_onError_tal``.

- Add support for Python 3.8 and 3.9.

- Drop support for Python 3.4.


4.4 (2018-10-05)
================

- Add support for Python 3.7.

4.3.1 (2018-03-21)
==================

- Host documentation at https://zopetal.readthedocs.io

- Fix a ``NameError`` on Python 3 in talgettext.py affecting i18ndude.
  See https://github.com/zopefoundation/zope.tal/pull/11

4.3.0 (2017-08-08)
==================

- Drop support for Python 3.3.

- Add support for Python 3.6.

4.2.0 (2016-04-12)
==================

- Drop support for Python 2.6 and 3.2.

- Accept and ignore ``i18n:ignore`` and ``i18n:ignore-attributes`` attributes.
  For compatibility with other tools (such as ``i18ndude``).

- Add support for Python 3.5.

4.1.1 (2015-06-05)
==================

- Suppress deprecation under Python 3.4 for default ``convert_charrefs``
  argument (passed to ``HTMLParser``).  Also ensures that upcoming change
  to the default in Python 3.5 will not affect us.

- Add support for Python 3.2 and PyPy3.

4.1.0 (2014-12-19)
==================

.. note::

   Support for PyPy3 is pending release of a fix for:
   https://bitbucket.org/pypy/pypy/issue/1946

- Add support for Python 3.4.

- Add support for testing on Travis.


4.0.0 (2014-01-13)
==================

- Fix possible UnicodeDecodeError in warning when msgid already exists.


4.0.0a1 (2013-02-15)
====================

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Add support for Python 3.3 and PyPy.

- Drop support for Python 2.4 and 2.5.

- Output attributes generate via ``tal:attributes`` and ``i18n:attributes``
  directives in alphabetical order.


3.6.1 (2012-03-09)
==================

- Avoid handling end tags within <script> tags in the HTML parser. This works
  around http://bugs.python.org/issue670664

- Fix documentation link in README.txt.

3.6.0 (2011-08-20)
==================

- Update `talinterpreter.FasterStringIO` to faster list-based implementation.

- Increase the default value of the `wrap` argument from 60 to 1023 characters,
  to avoid extra whitespace and line breaks.

- Fix printing of error messages for msgid conflict with non-ASCII texts.


3.5.2 (2009-10-31)
==================

- In ``talgettext.POEngine.translate``, print a warning if a msgid already
  exists in the domain with a different default.


3.5.1 (2009-03-08)
==================

- Update tests of "bad" entities for compatibility with the stricter
  HTMLParser module shipped with Python 2.6.x.


3.5.0 (2008-06-06)
==================

- Remove artificial addition of a trailing newline if the output doesn't end
  in one; this allows the template source to be the full specification of what
  should be included.
  (See https://bugs.launchpad.net/launchpad/+bug/218706.)


3.4.1 (2007-11-16)
==================

- Remove unnecessary ``dummyengine`` dependency on zope.i18n to
  simplify distribution.  The ``dummyengine.DummyTranslationDomain``
  class no longer implements
  ``zope.i18n.interfaces.ITranslationDomain`` as a result.  Installing
  zope.tal with easy_install or buildout no longer pulls in many
  unrelated distributions.

- Support running tests using ``setup.py test``.

- Stop pinning (no longer required) ``zope.traversing`` and
  ``zope.app.publisher`` versions in buildout.cfg.


3.4.0 (2007-10-03)
==================

- Update package meta-data.


3.4.0b1
=======

- Update dependency on ``zope.i18n`` to a verions requiring the correct
  version of ``zope.security``, avoiding a hidden dependency issue in
  ``zope.security``.

.. note::

   Changes before 3.4.0b1 where not tracked as an individual
   package and have been documented in the Zope 3 changelog.
