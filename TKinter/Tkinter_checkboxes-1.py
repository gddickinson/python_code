# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 21:50:33 2015

@author: george
"""

from Tkinter import *

master = Tk()
var1 = IntVar()
Checkbutton(master, text="male", variable=var1).grid(row=0, sticky=W)
var2 = IntVar()
Checkbutton(master, text="female", variable=var2).grid(row=1, sticky=W)
mainloop()