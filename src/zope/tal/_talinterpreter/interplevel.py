from pypy.interpreter.baseobjspace import ObjSpace


def _normalize(space, text):
    # Now we need to normalize the whitespace in implicit message ids and
    # implicit $name substitution values by stripping leading and trailing
    # whitespace, and folding all internal whitespace to a single space.
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    parts = [part for part in text.split(' ') if part]
    result = ' '.join(parts)
    return space.wrap(result)
_normalize.unwrap_spec = [ObjSpace, str]

