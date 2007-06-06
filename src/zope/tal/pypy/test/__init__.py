from pypy.interpreter.mixedmodule import MixedModule 

class Module(MixedModule):
    """A ZPT module."""

    interpleveldefs = {
        'test'        : 'zpt.test',
        'Interpreter' : 'zpt.Interpreter',
    }

    appleveldefs = {
    }
