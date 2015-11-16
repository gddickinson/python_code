# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 18:56:57 2015

@author: george
"""

def isAlphabeticalWord(word, wordList=None):
    if (len(word) > 0):
        curr = word[0]
    for letter in word:
        if (curr > letter):
            return False
        else:
            curr = letter
    if wordList is None:
        return True
    return word in wordList
    
print(isAlphabeticalWord('box'))