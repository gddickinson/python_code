# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:19:57 2015

@author: george
"""

def applyToEach(L,f):
    for i in range(len(L)):
        L[i] = f(L[i])

testList = [1, -4, 8, -9]


##########
#def timesFive(a):
#    return a * 5

#def addOne(a):
#    return a+1

def square(a):
    return a*a

applyToEach(testList, square)

print testList
