.. include:: ../README.rst

Using ``zope.tal`` requires three steps: choosing an expression engine
(usually :mod:`zope.tales`), creating a generator and parser, and then
interpreting the compiled program::

    from io import StringIO
    from zope.tal.talgenerator import TALGenerator
    from zope.tal.htmltalparser import HTMLTALParser
    from zope.tal.talinterpreter import TALInterpreter

    compiler = None # Will use a compiler for a dummy language
    source_file = '<string>'
    source_text = '<html><body><p>Hi</p></body></html>'
    gen = TALGenerator(compiler, source_file=source_file)
    parser = TALParser(gen)
    parser.parseString(source_text)
    program, macros = parser.getCode()

    output = StringIO()
    context = None # Usually will create a zope.tales context
    interpreter = TALInterpreter(self.program, macros, context, stream=output)
    interpreter()
    result = output.getvalue()

These aspects are all brought together in :mod:`zope.pagetemplate`.

API Documentation:

.. toctree::
   :maxdepth: 2

   interfaces
   taldefs
   talgenerator
   htmltalparser
   talparser
   talinterpreter

.. toctree::
   :maxdepth: 1

   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
