# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 22:03:07 2015

@author: george
"""

#We demonstrate in our first example, how to draw a line. 
#The method create_line(coords, options) is used to draw a straight line. The coordinates "coords" are given as four integer numbers: x1, y1, x2, y2 This means that the line goes from the point (x1, y1) to the point (x2, y2) After these coordinates follows a comma separated list of additional parameters, which may be empty. We set for example the colour of the line to the special green of our website: fill="#476042" 
#We kept the first example intentionally very simple. We create a canvas and draw a straight horizontal line into this canvas. This line vertically cuts the canvas into two areas. 
#The casting to an integer value in the assignment "y = int(canvas_height / 2)" is superfluous, because create_line can work with float values as well. They are automatically turned into integer values. In the following you can see the code of our first simple script: 


from Tkinter import *
master = Tk()

canvas_width = 80
canvas_height = 40
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
w.pack()

y = int(canvas_height / 2)
w.create_line(0, y, canvas_width, y, fill="#476042")


mainloop()