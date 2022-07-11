# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:29:25 2015

@author: george
"""

from Tkinter import *
# if you are working under Python 3, comment the previous line and comment out the following line
#from tkinter import *

#To initialize Tkinter, we have to create a Tk root widget, which is a window with a title bar and other decoration provided by the window manager. The root widget has to be created before any other widgets and there can only be one root widget.
root = Tk()
#The next line of code contains the Label widget. The first parameter of the Label call is the name of the parent window, in our case "root". So our Label widget is a child of the root widget. The keyword parameter "text" specifies the text to be shown:
w = Label(root, text="Hello Tkinter!")
#The pack method tells Tk to fit the size of the window to the given text.
w.pack()
#The window won't appear until we enter the Tkinter event loop:
root.mainloop()