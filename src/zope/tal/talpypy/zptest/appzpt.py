
import zope.tal
import random

def appfunc():
    return zope.tal.zptest.test(random.randrange(3))

#
# the code hereunder doesn't work : 
# it results in an ImportError
#
# from zope.tal import zptest
# import random

# def appfunc():
#     return zptest.test(random.randrange(3))

