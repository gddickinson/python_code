# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 16:04:58 2015

@author: george
"""
import string
    
def isWordIn(word, text):
    text = text.lower()
    temp = ''
    lowerWord = word[:]
    lowerWord = lowerWord.lower()
    splitChars = string.punctuation
    for letter in text:
        for char in splitChars:
            if letter == char:
                temp = temp + ' '
        
        temp = temp + letter
                        
    splitText = []
    splitText = temp.split()
    print splitText
    for testword in splitText:
        if testword == lowerWord:
            return True          
    return False

print (isWordIn('monkey','monkey-s  banana'))
 
