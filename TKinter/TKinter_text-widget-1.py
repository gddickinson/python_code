# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 05:55:15 2015

@author: george
"""

#==============================================================================
# We create a text widget by using the Text() method. We set the height to 2, i.e. two lines and the width to 30, i.e. 30 characters. We can apply the method insert() on the object T, which the Text() method had returned, to include text. We add two lines of text. 
#==============================================================================


from tkinter import *

root = Tk()
T = Text(root, height=2, width=30)
T.pack()
T.insert(END, "Just a text Widget\nin two lines\n")
mainloop()