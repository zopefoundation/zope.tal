try:
    from pypy.interpreter.mixedmodule import testmodule
    rptalinterpreter =  testmodule('rptalinterpreter', 'zope.tal')
except ImportError:
    import rptalinterpreter


normalize = rptalinterpreter.normalize
TALInterpreter = rptalinterpreter.TALInterpreter

