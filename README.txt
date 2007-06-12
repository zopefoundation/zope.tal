zope.tal Package Readme
=======================

Overview
--------

The Zope3 Template Attribute Language (TAL) specifies the custom namespace
and attributes which are used by the Zope Page Templates renderer to inject
dynamic markup into a page.  It also includes the Macro Expansion for TAL
(METAL) macro language used in page assembly.

The dynamic values themselves are specified using a companion language,
TALES (see the 'zope.tales' package for more).

See: http://www.zope.org/Wikis/DevSite/Projects/ZPT/TAL%20Specification%201.4

Getting PyPy
------------

Check out the latest version of PyPy:

  http://codespeak.net/pypy/dist/pypy/doc/getting-started.html#svn-check-out-run-the-latest-pypy-as-a-two-liner

Also make sure ctypes is available for your Python.

Running the tests
-----------------

To run the tests:

  $ python2.4 bootstrap.py
  $ bin/buildout
  $ export PYTHONPATH=/path/to/pypy-dist:$PYTHONPATH
  $ bin/test

Compiling with PyPy's RPython
-----------------------------

To compile the rpython:

First, you need to set up PYTHONPATH so it has the required packages on the
path:

  $ export PYTHONPATH=/path/to/buildout/src:/path/to/buildout/eggs/zope.interface:/path/to/buildout/eggs/zope.i18nmessageid:$PYTHONPATH

Now, run the following command to compile::

  $ python /path/to/pypy-dist/pypy/bin/compilemodule.py _talinterpreter zope.tal

The first argument is name of the RPython sub-package you want to
compile, the second argument is path to the package where this RPython
sub-package is found.

The compiled module will be placed in
/tmp/usession-XX/_talinterpreter/_talinterpreter.so. Move this file to
src/zope/tal and rename _talinterpreter the package to make this work.
