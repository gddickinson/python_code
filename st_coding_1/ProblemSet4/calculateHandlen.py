# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 23:07:11 2015

@author: george
"""

def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    # TO DO... <-- Remove this comment when you code this function
    values = hand.values()
    ans = sum(values)
    return ans
  
hand = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':2, 'n':1, 'g':1, 's':1}   
print (calculateHandlen(hand))