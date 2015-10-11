# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 18:20:53 2015

@author: george
"""

def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError, e:
        print "division by zero! " + str(e)
    else:
        print "result is", result
    finally:
        print "executing finally clause"

divide(2,1)