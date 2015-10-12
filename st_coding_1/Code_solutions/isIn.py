# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 10:12:31 2015

@author: george
"""

def isIn(char, aStr):
    char = char.lower()
    aStr = aStr.lower()
    half = len(aStr)/2
    test = aStr[half-1:half]
    #print (aStr)
    if char == aStr:
        return True
    if char == test:
        return True
    if test == '':
        return False
    else:
        if char < test:
            return isIn(char, aStr[0:half])
            n = len(aStr)
            while test == aStr[n-1:n]:
                aStr = aStr[0:n-1]
        if char > test:
            return isIn(char, aStr[half:])
            while test == aStr[0:0+1]:
                aStr = aStr[0+1:]
                       
print (isIn('a', 'abbbccccddddeeefff'))
