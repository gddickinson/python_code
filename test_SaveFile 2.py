# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 19:26:54 2017

@author: George
"""

f = open("deleteMe.txt")
content = f.read()
f.close()

words = content.split()
print("There are {0} words in the file.".format(len(words)))