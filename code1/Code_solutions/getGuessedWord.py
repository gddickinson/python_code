# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 09:03:46 2015

@author: george
"""

def getGuessedWord(secretWord, lettersGuessed):
    def testLetter (letter, lettersGuessed):
        i = (len(lettersGuessed))-1           
        while i >= 0:
            if letter == lettersGuessed[i]:
                return letter
            i -=1                       
        return ' _'
    
    length = (len(secretWord))
    i = length -1
    ans =""
    while i >= 0:
        ans = ans + testLetter(secretWord[i], lettersGuessed)
        i -=1
    return ans[::-1]
    
    
    
print getGuessedWord('apple' ,['e', 'i', 'k', 'p', 'r', 's'])