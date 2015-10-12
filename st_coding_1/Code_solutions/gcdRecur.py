# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 12:50:19 2015

@author: george
"""

def gcdRecur(a,b):
    if b == 0:
        return a
    
    else:
        return gcdRecur(b, a%b)
        
print (gcdRecur(17,12))
    