# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 06:09:04 2015

@author: george
"""

import sys
if sys.version_info < (3, 0):
    from Tkinter import *
else:
    from tkinter import *
from tkMessageBox import *

def answer():
    showerror("Answer", "Sorry, no answer available")

def callback():
    if askyesno('Verify', 'Really quit?'):
        showwarning('Yes', 'Not yet implemented')
    else:
        showinfo('No', 'Quit has been cancelled')

Button(text='Quit', command=callback).pack(fill=X)
Button(text='Answer', command=answer).pack(fill=X)
mainloop()