try:
    from pypy.interpreter.mixedmodule import testmodule
    _talinterpreter =  testmodule('_talinterpreter', 'zope.tal')
except AttributeError:
    import _talinterpreter
except ImportError:
    import _talinterpreter


normalize = _talinterpreter._normalize
TALInterpreter = _talinterpreter.TALInterpreter

