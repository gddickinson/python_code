# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 11:09:26 2015

@author: george
"""

def gdcIter(a,b):
    if a > b:
        c = b
        b = a
        a = c
    
    if a == b:
        return a
    
    testValue = a
    
    for testValue in range(a,0,-1):
        if a%testValue == 0 and b%testValue == 0:
            return testValue
        else:
            testValue -=1

    return 1

print (gdcIter(225,120))
        