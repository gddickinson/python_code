# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 00:31:05 2016

@author: george
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-


from tkinter import Tk, Frame, BOTH


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
         
        self.parent = parent
        self.parent.title("Centered window")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        

    def centerWindow(self):
      
        w = 290
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
  
    root = Tk()
    ex = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 