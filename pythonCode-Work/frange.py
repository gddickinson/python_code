# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 09:44:36 2015

@author: George
"""

def frange(start, end=None, inc=None):

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L
   
print (frange(1.5,10,1.5))