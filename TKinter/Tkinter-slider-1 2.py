# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 05:49:48 2015

@author: george
"""

from Tkinter import *

master = Tk()
w = Scale(master, from_=0, to=42)
w.pack()
w = Scale(master, from_=0, to=200, orient=HORIZONTAL)
w.pack()

mainloop()