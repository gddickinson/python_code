# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 14:26:24 2015

@author: george
"""

def lenRecur(aStr):
        
    if aStr == '':
        return 0
    
    else:
        return 1+lenRecur(aStr[1:])

print (lenRecur('aaa'))