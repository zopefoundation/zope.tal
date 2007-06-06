from pypy.interpreter.mixedmodule import MixedModule 

class Module(MixedModule):
    """TALInterpreter module."""

    interpleveldefs = {
        'normalize'        : 'talinterpreter.normalize',
        'TALInterpreter' : 'talinterpreter.TALInterpreter',
    }

    appleveldefs = {
    }
