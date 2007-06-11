from pypy.interpreter.mixedmodule import MixedModule 

class Module(MixedModule):
    """interpreter module."""

    interpleveldefs = {
        '_normalize' : 'interplevel._normalize',
    }

    appleveldefs = {
        'TALInterpreter' : 'applevel.TALInterpreter',
        'normalize' : 'applevel.normalize',
    }


