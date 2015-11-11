# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:50:24 2015

@author: robot
"""

def stdDevOfLengths(L):
    """
    L: a list of strings

    returns: float, the standard deviation of the lengths of the strings,
      or NaN if L is empty.
    """

    ans = []
    if len(L) == 0:
        return float('NaN')
    
    for word in L:
        ans.append(len(word))
    
    mean = sum(ans)/float(len(ans))
    tot = 0.0
    for x in ans:
        tot += (x - mean)**2
    stDev = (tot/len(ans))**0.5    
    
    
    return stDev




L = ['apples', 'oranges', 'kiwis', 'pineapples']

print(stdDevOfLengths(L))