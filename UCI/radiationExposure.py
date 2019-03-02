# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:01:09 2015

@author: George
"""
def f(x):
	import math
	return 400*math.e**(math.log(0.5)/3.66 * x)


def radiationExposure(start, stop, step):
    
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
    
    ans = 0
    i = start
    integral = 0
    for i in frange(start,stop,step):
        integral = f(i)*step
        ans += integral
        i += step
        
    return ans
    
print (radiationExposure(0,4,0.25))