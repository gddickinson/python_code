# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:48:09 2015

@author: george
"""

#http://www.python-course.eu/tkinter_buttons.php

import sys
if sys.version_info < (3, 0):
    import Tkinter as tk
else:
    import tkinter as tk

counter = 0 
def counter_label(label):
  counter = 0
  def count():
    global counter
    counter += 1
    label.config(text=str(counter))
    label.after(1000, count)
  count()
 
 
root = tk.Tk()
root.title("Counting Seconds")
label = tk.Label(root, fg="dark green")
label.pack()
counter_label(label)
button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()
root.mainloop()