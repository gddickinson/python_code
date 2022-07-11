# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 17:40:25 2015

@author: george
"""

animals = {'a': ['aardvark'], 'b': ['baboon'], 'c': ['coati'], 'd': ['donkey','dog','dingo']}

def biggest(aDict):
    length = 0
    if aDict == {}:
        return None
    if len(aDict) == 1:
        answer = aDict.keys()
        return str(answer)[2:-2]
    for e in aDict:
        if len(aDict[e])>length:
            answer = e
            length = len(aDict[e])
    
    return answer
    

print (biggest(animals))