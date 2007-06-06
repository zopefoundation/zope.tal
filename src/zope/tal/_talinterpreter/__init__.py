from pypy.interpreter.mixedmodule import MixedModule 

class Module(MixedModule):
    """interpreter module."""

    interpleveldefs = {
        'normalize' : 'interplevel.normalize',
    }

    appleveldefs = {
        'TALInterpreter' : 'applevel.TALInterpreter',
    }


