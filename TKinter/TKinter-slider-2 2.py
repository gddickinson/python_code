# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 05:50:46 2015

@author: george
"""

from Tkinter import *

def show_values():
    print (w1.get(), w2.get())

master = Tk()
w1 = Scale(master, from_=0, to=42)
w1.pack()
w2 = Scale(master, from_=0, to=200, orient=HORIZONTAL)
w2.pack()
Button(master, text='Show', command=show_values).pack()

mainloop()