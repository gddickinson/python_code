# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 20:26:00 2015

@author: george
"""

def factR(n):
    """assumes that n is an int > 0
       returns n!"""
    if n == 1:
        return n
    return n*factR(n-1)
    
print (factR(500))
