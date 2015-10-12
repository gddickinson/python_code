# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 19:50:40 2015

@author: george
"""

def iterPower (base, exp):
    result = 1
    while exp > 0:
        result *= base
        exp -= 1
    return result

print iterPower(2.5, 3)