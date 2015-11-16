# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 12:12:47 2015

@author: george
"""

def intersect(L1, L2):
    tmp = []
    for e1 in L1:
        for e2 in L2:
            if e1 == e2:
                tmp.append(e1)
    res = []
    for e in tmp:
        if not(e in res):
            res.append(e)
    return res

#Quadratic complexity i.e O(len(L1)*len(L2))	
    
x = [1,2,3,4,5,6,7,8,9]
y = [2,5,9]

print intersect(x,y)