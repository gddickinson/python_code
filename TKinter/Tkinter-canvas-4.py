# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 22:07:29 2015

@author: george
"""

from Tkinter import *

canvas_width = 190
canvas_height =150

master = Tk()

w = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
w.pack()

w.create_oval(50,50,100,100)

#We can define a small function drawing circles by using the create_oval() method.
#==============================================================================
# def circle(canvas,x,y, r):
#    id = canvas.create_oval(x-r,y-r,x+r,y+r)
#    return id
#==============================================================================


mainloop()