# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:11:12 2015

@author: george
"""

def f(n):
   """
   n: integer, n >= 0.
   """
   if n == 0:
      return 1
   else:
      return n * f(n-1)

