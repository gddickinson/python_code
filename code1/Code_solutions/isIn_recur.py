# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:19:41 2015

@author: george
"""

def isIn(a, s):
   '''
   a is a character, or, singleton string.
   s is a string, sorted in alphabetical order.
   '''
   if len(s) == 0:
      return False
   elif len(s) == 1:
      return a == s
   else:
      test = s[len(s)/2]
      if test == a:
         return True
      elif a < test:
         return isIn(a, s[:len(s)/2])
      else:
         return isIn(a, s[len(s)/2+1:])


a= 'f'
s = 'dsgrwhsfdgtwtrjshfatruyoufgfdf'
print isIn(a,s)