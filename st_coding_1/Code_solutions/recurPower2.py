# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 20:26:00 2015

@author: george
"""

def recurPowerNew(base, exp):
    if exp == 0:
        return 1

    elif exp%2 == 1: 
        return base*recurPowerNew(base, exp-1)

    else:
        return recurPowerNew(base*base, (exp/2))
        

print (recurPowerNew(16, 2))

