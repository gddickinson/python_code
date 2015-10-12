# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 09:10:26 2015

@author: george
"""

def lessThan4(aList):
    '''
    aList: a list of strings
    '''
    ans = []
    for item in aList:
        if len(item) <4:
            ans.append(item)
    
    return ans
   


aList = ["apple", "cat", "dog", "banana"]
print lessThan4(aList)    