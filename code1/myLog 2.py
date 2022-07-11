# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 15:18:54 2015

@author: george
"""

def myLog(x, b):
    '''
    x: a positive integer
    b: a positive integer; b >= 2

    returns: log_b(x), or, the logarithm of x relative to a base b.
    '''
    
    result = 0
    count = b
    
    if b>x:
        return 0
    
    if x/b < b:
        return 1
    
    if x%b == 0:
        result = 1
        while b < x:
            result +=1
            b = b * count           
        
    elif x%b ==1:
        while b  < x:
            result +=1
            b = b * count
    
    else:
        result = 1
        if b  < x:
            result +=1
            b = b * count        
    return result
        
    
print (myLog(27,3))
print (myLog(26,3))
print (myLog(28,3))
print (myLog(4,16))
print (myLog(13,2))
print (myLog(20,5))
print (myLog(86,2))
