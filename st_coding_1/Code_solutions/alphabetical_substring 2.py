# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 11:21:49 2015

@author: george
"""

s = 'abcbcd'
answer = ''
answerlength = len(answer)

def checkAlphabetical(string2):
    for i in range(len(string2) - 1):
        if string2[i] > string2[i + 1]:
            return False
    return True

def longestAlpha(string1):
    length=len(s)
    end = 1
    ans=''
    while end <= length:    
        newstring = string1[0:end]
        if checkAlphabetical(newstring) == True and len(newstring) > len(ans):
            ans = newstring
        end +=1
    #print (ans)
    return ans

for i in range(len(s)):
    newstring1 = s[i:]
    #print (newstring1)
    answer1 = longestAlpha(newstring1)
    if len(answer1) > len(answer):
        answer = answer1



print ("Longest substring in alphabetical order is:" +str(answer))