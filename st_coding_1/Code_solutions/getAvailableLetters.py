# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:21:17 2015

@author: george
"""

def getAvailableLetters(lettersGuessed):
    import string
    alpha = string.ascii_lowercase
    def testLetter (letter, lettersGuessed):
        i = (len(lettersGuessed))-1           
        while i >= 0:
            if letter == lettersGuessed[i]:
                return True
            i -=1                       
        return False
    
    ans = ''    
    i = 25
    while i >=0:
        if testLetter(alpha[i], lettersGuessed) == True:
            addLetter = ''
        else:
            addLetter = alpha[i]
        ans = ans + addLetter
        i-=1
        
    return ans[::-1]

lettersGuessed = ['l', 'i', 'k', 'p', 'r', 's']
print getAvailableLetters(lettersGuessed)