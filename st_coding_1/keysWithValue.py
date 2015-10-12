# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 09:34:44 2015

@author: george
"""

def keysWithValue(aDict, target):
    '''
    aDict: a dictionary
    target: an integer
    '''
    ans = []
    for key in aDict:
        if aDict[key] == target:
          ans.append(key)
    ans.sort()
    
    return ans


aDict = {2:10, 8:10, 3:10, 1:40, 5:50, 6:60}
print(keysWithValue(aDict, 10))