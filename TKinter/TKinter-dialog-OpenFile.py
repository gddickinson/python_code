# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 06:11:03 2015

@author: george
"""

from Tkinter import *
from tkFileDialog   import askopenfilename      

def callback():
    name= askopenfilename() 
    print name
    
errmsg = 'Error!'
Button(text='File Open', command=callback).pack(fill=X)
mainloop()