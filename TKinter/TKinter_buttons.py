# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:46:33 2015

@author: george
"""

#http://www.python-course.eu/tkinter_buttons.php

from Tkinter import *
class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.pack(side=LEFT)
    self.slogan = Button(frame,
                         text="Hello",
                         command=self.write_slogan)
    self.slogan.pack(side=LEFT)
  def write_slogan(self):
    print "Tkinter is easy to use!"

root = Tk()
app = App(root)
root.mainloop()