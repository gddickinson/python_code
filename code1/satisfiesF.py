# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 10:29:11 2015

@author: george
"""
def f(s):
    return 'b' in s

L = ['a', 'a', 'a']

########

def satisfiesF(L):
    """
    Assumes L is a list of strings
    Assume function f is already defined for you and it maps a string to a Boolean
    Mutates L such that it contains all of the strings, s, originally in L such
            that f(s) returns True, and no other elements
    Returns the length of L after mutation
    """
    
    for x in L:

        if f(x) == False:
            index = L.index(x)
        
            del L[index]
    
    return len(L)
            
    
def run_satisfiesF(L, satisfiesF):

    print satisfiesF(L)
    print L

run_satisfiesF(L, satisfiesF)