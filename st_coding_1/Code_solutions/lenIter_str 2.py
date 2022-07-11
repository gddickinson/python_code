# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 14:13:15 2015

@author: george
"""

def lenIter(aStr):
    ans = 0
    while aStr != "":
        ans +=1
        aStr = aStr[1:]
    
    return ans
    
print (lenIter(""))