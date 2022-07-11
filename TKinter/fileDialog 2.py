# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 10:48:22 2018

@author: George
"""

from tkinter import filedialog
from tkinter import *
from tkinter import Tk, Frame, BOTH
from tkinter import Tk, Label, Button

class Base_Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
         
        self.parent = parent
        
        self.initUI()
        
    
    def initUI(self):
      
        self.parent.title("Test")
        self.pack(fill=BOTH, expand=1)
 

        self.label = Label(self.parent, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(self.parent, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(self.parent, text="Close", command=self.parent.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")       

def main():
  
    root = Tk()
    root.geometry("250x150+300+300")
    app = Base_Window(root)
    root.mainloop()  


if __name__ == '__main__':
    main()





#root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
#print (root.filename)