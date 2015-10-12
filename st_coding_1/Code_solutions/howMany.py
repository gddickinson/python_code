# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 17:40:25 2015

@author: george
"""

animals = {'a': ['aardvark'], 'b': ['baboon'], 'c': ['coati'], 'd': ['donkey','dog','dingo']}

def howMany(aDict):
    answer = 0
    for e in aDict:
        answer += len(aDict[e])
    
    return answer
    

print (howMany(animals))