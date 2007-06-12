
import zope.tal
import random

def appfunc():
    return zope.tal.zptest.test(random.randrange(3))

