# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 10:40:59 2018

@author: George
"""

from tkinter import Tk, Label, Button
from tkinter import filedialog

class visioMod:
    def __init__(self, master):
        self.master = master
        master.title("Visio CEM Diagram Link/Node Display App")

        self.label = Label(master, text="Testing!")
        self.label.pack()

        self.openFile_button = Button(master, text="Open File", command=self.openFile)
        self.openFile_button.pack()

        self.close_button = Button(master, text="Quit", command=master.destroy)
        self.close_button.pack()

    def openFile(self):
        filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        print (filename)


def main(): 
    root = Tk()
    root.geometry("500x500")
    app = visioMod(root)
    root.mainloop()  


if __name__ == '__main__':
    main()