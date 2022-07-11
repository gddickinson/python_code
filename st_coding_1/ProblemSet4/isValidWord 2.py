# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 07:56:44 2015

@author: george
"""

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    # TO DO ... <-- Remove this comment when you code this function
    hand2 = hand.copy()
    wordlength = len(word)    
    for testword in wordList:
        if testword == word:
            for letter in word:
                if hand2.get(letter,0) > 0:
                    hand2[letter] = hand2.get(letter, 0) - 1
                    wordlength -= 1
                else:
                    return False
            if wordlength == 0:
                return True
            else:
                return False
    else:
        return False        


wordList = loadWords()
word = 'sing'
hand = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':2, 'n':1, 'g':1, 's':1}   

print isValidWord(word, hand, wordList)