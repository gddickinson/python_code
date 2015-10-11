# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 20:39:08 2015

@author: george
"""

import string
import random

WORDLIST_FILENAME = "words.txt"

def isWord(wordList, word):
    """
    Determines if word is a valid word.

    wordList: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordList.

    Example:
    >>> isWord(wordList, 'bat') returns
    True
    >>> isWord(wordList, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in wordList
    
def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = inFile.read().split()
    print "  ", len(wordList), "words loaded."
    return wordList


def buildCoder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation, numbers and spaces.

    shift: 0 <= int < 26
    returns: dict
    """
    answer = {}
    lowerCase, upperCase = [], []
    for letter in string.ascii_lowercase:
        lowerCase.append(letter)
    for letter in string.ascii_uppercase:
        upperCase.append(letter)
    shiftLowerCase = lowerCase[shift:]+lowerCase[:shift]
    shiftUpperCase = upperCase[shift:]+upperCase[:shift]
    
    for i in range(26):
        answer[upperCase[i]] = shiftUpperCase[i]
        answer[lowerCase[i]] = shiftLowerCase[i]
    
    return answer

def applyCoder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text
    """
    answer = ''
    for char in text:
        try:
            answer += coder[char]
        except:
            answer += char
    
    return answer

def applyShift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. Lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.

    text: string to apply the shift to
    shift: amount to shift the text (0 <= int < 26)
    returns: text after being shifted by specified amount.
    """
    return applyCoder(text, buildCoder(shift))
    
def findBestShift(wordList, text):
    """
    Finds a shift key that can decrypt the encoded text.

    text: string
    returns: 0 <= int < 26
    """
    #make variable to store answer
    answer = 0    
    #make variable to record shiftNumber
    shiftNumber = 0
    #make variable to count number of words in list
    validWordHit = 0
    mostHits = 0
    #make variable to store shiftedText
    shiftedText = ''
    #apply shift over loop
    while shiftNumber < 26:
        shiftedText = applyShift(text,(shiftNumber))        
        #make variable to store text words
        encrypted_word_list = []                
        encrypted_word_list = shiftedText.split(' ')
        #print encrypted_word_list
        for word in encrypted_word_list:
            if isWord(wordList,word):
                validWordHit +=1
                #print validWordHit, shiftNumber
        if validWordHit > mostHits:
            mostHits = validWordHit
            answer = shiftNumber
        shiftNumber +=1
        validWordHit = 0

    #return shiftNumber that gives most number of valid words    
    return answer

wordList = loadWords()
print findBestShift(wordList, 'Pmttw, ewztl!')










