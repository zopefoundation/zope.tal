try:
    from pypy.interpreter.mixedmodule import testmodule
    _talinterpreter =  testmodule('_talinterpreter', 'zope.tal')
except ImportError:
    import _talinterpreter

normalize = _talinterpreter.normalize
TALInterpreter = _talinterpreter.TALInterpreter
