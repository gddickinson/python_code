# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 09:18:08 2015

@author: george
"""

def sumDigits(N):
    '''
    N: a non-negative integer
    '''
    if N < 10:
        return N
        
    else:
        return sumDigits (N%10) + sumDigits(N/10)
        
print sumDigits(929)