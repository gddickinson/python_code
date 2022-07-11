# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 11:49:45 2015

@author: george
"""
def isSubset(L1, L2):
    for e1 in L1:
        matched = False
        for e2 in L2:
            if e1 == e2:
                matched = True
                break
        if not matched:
            return False
    return True


#Demostrates quadratic complexity i.e O(len(L1)**2)
x = [2,3,4]
y = [1,2,3,4]
print isSubset(x,y)