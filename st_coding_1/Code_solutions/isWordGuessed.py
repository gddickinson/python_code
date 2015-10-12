# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 21:11:27 2015

@author: george
"""

def isWordGuessed(secretWord, lettersGuessed):
    def testLetter (letter, lettersGuessed):
        i = (len(lettersGuessed))-1           
        while i >= 0:
            if letter == lettersGuessed[i]:
                return True
            i -=1                       
        return False
    
    length = (len(secretWord))
    i = length -1
    correct =0
    while i >= 0:
        print(secretWord[i])
        if testLetter(secretWord[i], lettersGuessed) == False:
            return False
        else:
            correct +=1
        i -=1
    #print (length)
    #print (correct)    
    #print (i)
    if correct == length:
        return True   
        
    else:
        return False
    #print(testLetter('a', lettersGuessed))

print (isWordGuessed('test', ['t', 's', 'l', 'e'] ))

        