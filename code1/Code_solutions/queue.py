# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 19:21:58 2015

@author: george
"""

class Queue(object):
    """An intSet is a set of integers
    The value is represented by a list of ints, self.vals.
    Each int in the set occurs in self.vals exactly once."""

    def __init__(self):
        """Create an empty set of integers"""
        self.vals = []

    def insert(self, e):
        """Assumes e is an integer and inserts e into self""" 
        self.vals.append(e)

    def member(self, e):
        """Assumes e is an integer
           Returns True if e is in self, and False otherwise"""
        return e in self.vals

    def remove(self):
        """pops from end"""
        try:        
            result = self.vals.pop()
            return result
        except:
            raise ValueError('List empty')

    def __str__(self):
        """Returns a string representation of self"""
        self.vals.sort()
        return '{' + ','.join([str(e) for e in self.vals]) + '}'
           
    def __len__(self):
        return len(self.vals)
        

s= Queue()
for i in range(2):
    s.insert(i)

print s
   
print s.remove()
print s.remove()
print s.remove()