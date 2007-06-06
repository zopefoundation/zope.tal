from pypy.interpreter.baseobjspace import ObjSpace

def normalize(space, text):
    # Now we need to normalize the whitespace in implicit message ids and
    # implicit $name substitution values by stripping leading and trailing
    # whitespace, and folding all internal whitespace to a single space.
    result = ' '.join(text.split())
    return space.wrap(result)
normalize.unwrap_spec = [ObjSpace, str]

