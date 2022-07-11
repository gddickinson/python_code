# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 16:04:08 2015

@author: george
"""

def search(L, e):
    for i in range(len(L)):
        if L[i] == e:
            return True
        if L[i] > e:
            return False
    return False

def newsearch(L, e):
    size = len(L)
    for i in range(size):
        if L[size-i-1] == e:
            return True
        if L[i] < e:
            return False
    return False

L = [0,1,2,3]
e = 0

print (search(L,e))
print (newsearch (L,e))
