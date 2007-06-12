from pypy.interpreter.baseobjspace import ObjSpace, W_Root, Wrappable
from pypy.interpreter.gateway import interp2app
from pypy.interpreter.typedef import TypeDef, GetSetProperty

def importModule(space, name):
    w_builtin = space.getbuiltinmodule('__builtin__')
    w_import = space.getattr(w_builtin, space.wrap('__import__'))
    w_module = space.call_function(w_import, space.wrap(name))
    return w_module

def test(space, n):
    return space.wrap(n + 1)
test.unwrap_spec = [ObjSpace, int]

class Interpreter(Wrappable):
    def __init__(self, space, w_instance, code=1):
        self.space = space
        self.code = code
        self.w_instance = w_instance

    def multiply(self, w_y):
        space = self.space
        y = space.int_w(w_y)
        return space.wrap(self.code * y)

    def fget_code(space, self):
        return space.wrap(self.code)

    def fset_code(space, self, w_value):
        self.code = space.int_w(w_value)

    def call(self):
        space = self.space
        w_random = importModule(space, 'random')
        w_randrange = space.getattr(w_random, space.wrap('randrange'))
        rand = space.call_function(w_randrange, space.wrap(self.code))
        return rand

    def power2(self):
        p = Power2(self.code)
        return self.space.wrap(p.compute())

    def getInstance(self):
        space = self.space
        if space.is_w(self.w_instance, space.wrap(None)):
            return
        w_append =space.getattr(self.w_instance, 'append')
        space.call_function(w_append, space.wrap(3))
        return self.w_instance

class Power2:
    def __init__(self, value):
        self.value = value

    def compute(self):
        return self.value * self.value



def interpreter_new(space, w_subtype, w_instance, x):
    return space.wrap(Interpreter(space, w_instance, x))
interpreter_new.unwrap_spec = [ObjSpace, W_Root, W_Root, int]

getset_code = GetSetProperty(Interpreter.fget_code, Interpreter.fset_code, cls=Interpreter)

Interpreter.typedef = TypeDef('Interpreter',
    __new__ = interp2app(interpreter_new),
    code = getset_code,
    multiply = interp2app(Interpreter.multiply),
    __call__ = interp2app(Interpreter.call),
    power2 = interp2app(Interpreter.power2),
    getInstance = interp2app(Interpreter.getInstance),
)
