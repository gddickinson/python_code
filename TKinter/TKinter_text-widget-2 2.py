# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 05:57:01 2015

@author: george
"""

from Tkinter import *

root = Tk()
T = Text(root, height=2, width=30)
T.pack()
quote = """HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished."""
T.insert(END, quote)
mainloop()