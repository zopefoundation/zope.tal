from pypy.interpreter.mixedmodule import MixedModule 

class Module(MixedModule):
    """interpreter module."""

    interpleveldefs = {
    }

    appleveldefs = {
        'TALInterpreter' : 'applevel.TALInterpreter',
        'normalize' : 'applevel.normalize',
    }
