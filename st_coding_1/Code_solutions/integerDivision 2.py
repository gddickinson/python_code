# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 18:59:11 2015

@author: george
"""

def integerDivision(x, a):
    """
    x: a non-negative integer argument
    a: a positive integer argument

    returns: integer, the integer division of x divided by a.
    """
    count = 0    
    while x >= a:
        count += 1
        x = x - a
    return count

print integerDivision(1,5)