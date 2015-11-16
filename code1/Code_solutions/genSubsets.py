# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 12:18:02 2015

@author: george
"""

def genSubsets(L):
    res = []
    if len(L) == 0:
        return [[]] #list of empty list
    smaller = genSubsets(L[:-1])
    # get all subsets without last element
    extra = L[-1:]
    # create a list of just last element
    new = []
    for small in smaller:
        new.append(small+extra)
    # for all smaller solutions, add one with last element
    return smaller+new
    # combine those with last element and those without
    
# Exponential complexity O(2**L)

x = [0,1,2]    
y = [0,1,2,3]
z = ['A','B','C','D','E','F','G','H','I','J']

print genSubsets(z)