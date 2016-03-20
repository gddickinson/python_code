# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 21:50:33 2015

@author: george
"""

import sys
if sys.version_info < (3, 0):
    from Tkinter import *
else:
    from tkinter import *

master = Tk()
var1 = IntVar()
Checkbutton(master, text="male", variable=var1).grid(row=0, sticky=W)
var2 = IntVar()
Checkbutton(master, text="female", variable=var2).grid(row=1, sticky=W)
mainloop()