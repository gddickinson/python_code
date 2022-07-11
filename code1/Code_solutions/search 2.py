# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 15:28:33 2015

@author: george
"""

def search(L, e):
    for i in range(len(L)):
        if L[i] == e:
            return True
        if L[i] > e:
            return False
    return False


def search3(L, e):
    if L[0] == e:
        return True
    elif L[0] > e:
        return False
    else:
        return search3(L[1:], e)

L = []
e = 15
print (search (L,e))
print (search3(L,e))