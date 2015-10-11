# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 19:21:58 2015

@author: george
"""

class intSet(object):
    """An intSet is a set of integers
    The value is represented by a list of ints, self.vals.
    Each int in the set occurs in self.vals exactly once."""

    def __init__(self):
        """Create an empty set of integers"""
        self.vals = []

    def insert(self, e):
        """Assumes e is an integer and inserts e into self""" 
        if not e in self.vals:
            self.vals.append(e)

    def member(self, e):
        """Assumes e is an integer
           Returns True if e is in self, and False otherwise"""
        return e in self.vals

    def remove(self, e):
        """Assumes e is an integer and removes e from self
           Raises ValueError if e is not in self"""
        try:
            self.vals.remove(e)
        except:
            raise ValueError(str(e) + ' not found')

    def __str__(self):
        """Returns a string representation of self"""
        self.vals.sort()
        return '{' + ','.join([str(e) for e in self.vals]) + '}'
        
    
    def intersect(self,other):
        tmp = []
        for e1 in self.vals:
            for e2 in other.vals:
                if e1 == e2:
                    tmp.append(e1)
        result = []
        for e in tmp:
            if not(e in result):
                result.append(e)
        return '{' + ','.join([str(e) for e in result]) + '}'
    
    def __len__(self):
        return len(self.vals)
        
s1 = intSet()
s2 = intSet()
for i in range(10):
    s1.insert(i)
    s2.insert(i)
s2.remove(5)
s2.remove(9)  
   
print s1.intersect(s2)