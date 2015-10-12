# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 14:48:13 2015

@author: george
"""

def Square(x):
    return SquareHelper(abs(x), abs(x))

def SquareHelper(n, x):
    if n == 0:
        return 0
    return SquareHelper(n-1, x) + x
    
print (Square(1.5))