# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 07:44:09 2015

@author: george
"""

def f(x):
    import math
    return 10*math.e**(math.log(0.5)/5.27 * x) #cobalt-60
    #return 400*math.e**(math.log(0.5)/3.66 * x) #radium-224
    #return 200*math.e**(math.log(0.5)/14.1 * x) #uranium-240
    #return 150*math.e**(math.log(0.5)/32.2 * x) #cesium-138
    #return 60*math.e**(math.log(0.5)/55.6 * x) #rado-220

def radiationExposure(start, stop, step):
    '''
    Computes and returns the amount of radiation exposed
    to between the start and stop times. Calls the 
    function f (defined for you in the grading script)
    to obtain the value of the function at any point.
 
    start: integer, the time at which exposure begins
    stop: integer, the time at which exposure ends
    step: float, the width of each rectangle. You can assume that
      the step size will always partition the space evenly.

    returns: float, the amount of radiation exposed to 
      between start and stop times.
    '''

    
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


print (radiationExposure(40,100,1.5))