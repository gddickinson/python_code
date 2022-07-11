# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 00:41:23 2016

@author: george
"""

from __future__ import print_function
from tkinter import Tk, Text, BOTH, W, N, E, S, INSERT, Scrollbar, RIGHT, Y, WORD, END
from tkinter.ttk import Frame, Button, Label, Style, Combobox
from tkinter.filedialog import askopenfilename
from os import path
import sys, getopt, re
import tkinter.scrolledtext as tkst

class Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()
        
        
    def initUI(self):
      
        self.parent.title("Citation Search Tool")
        self.pack(fill=BOTH, expand=True)
        
        self.inputFile = ''
        self.outputFile = ''
        self.startCharacter = '('
        self.endCharcter = ')'

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        self.numberCharcters = 30
        
        lbl = Label(self, text="Searches .txt files")
        lbl.grid(sticky=W, pady=4, padx=5)
        
        self.area = tkst.ScrolledText(master = self, wrap= WORD, width= 20, height= 10)
        self.area.grid(row=1, column=0, columnspan=3, rowspan=4, padx=5, sticky=E+W+S+N)
        

        cbtn = Button(self, text="Select file and search",command=self.getFileName)
        cbtn.grid(row=2, column=3, pady=4)
                
        
        #combobox
#        label1Top = Label(self,text = "Start Charcter: ")
#        label1Top.grid(column=0, row=5)        
#        startCharcter_box = Combobox(self, values=["(", "[","{"])
#        startCharcter_box.current(0)
#        startCharcter_box.grid(column=1, row=5, sticky=W,padx=5)
#    
#        label2Top = Label(self,text = "End Charcter: ")
#        label2Top.grid(column=2, row=5, sticky=W+E)        
#        endCharcter_box = Combobox(self, values=[")", "]","}"])
#        endCharcter_box.current(0)
#        endCharcter_box.grid(column=3, row=5, sticky=W,padx=5)

        label3Top = Label(self,text = "Number of characters to return: ")
        label3Top.grid(column=0, row=5)   
        self.numberCharacters_SpinBox = Combobox(self, values=list(range(0,100)))
        self.numberCharacters_SpinBox.set(self.numberCharcters)       
        self.numberCharacters_SpinBox.grid(column=1, row=5, sticky=W,padx=5)


    
    def search(self):    
        '''re search for text containing start and end characters, and preceeding n characters'''        
        try:
            searchFile = open(self.inputFile, "r")
            text = searchFile.read()
            searchFile.close()
        except:
            print('Unable to open input file')
        
        #find all occurences of text within parentheses
        #result = re.findall('\(.*?\)',text)
        result = re.findall('\{}.*?\{}'.format(self.startCharacter,self.endCharcter),text)
        
        #result2 = re.findall(r'(.*?)\(.*?\)',text)
        result2 = re.findall(r'{}.*?{}\{}.*?\{}'.format(self.startCharacter,self.endCharcter,self.startCharacter,self.endCharcter),text)
        result3 = []
        
        n = 0 - int(self.numberCharacters_SpinBox.get())
        
        for i in range(len(result)):
            if re.search('\d+',result[i]) and len(result[i]) > 4:
                result[i] = result[i].encode('ascii', 'replace').decode('ascii')
                result2[i] = result2[i].encode('ascii', 'replace').decode('ascii')
                try:
                    result3.append([result2[i][n:],result[i]])
                except:
                    result3.append([result2[i],result[i]])
        
        try:
            self.area.delete('1.0', END)
            saveFile = open(self.outputFile, 'w')
             
            for item in result3:
                print(*item,file=saveFile, sep=',') 
                self.area.insert(INSERT, item)
                self.area.insert(END,'\n')
            saveFile.close()
            
        except:
            print('Unable to write results file')
    
        print('search finished')
             

    def getFileName(self):
        self.inputFile = askopenfilename(filetypes = (("text files","*.txt"),("all files","*.*"))) 
        #self.outputFile = path.dirname(self.inputFile)
        pathName, fileName = path.split(self.inputFile)
        outName = fileName.split('.')[0] + '_searchResult.txt'
        self.outputFile = path.join(pathName, outName)
        print(self.inputFile)
        print(self.outputFile)
        #run search
        self.search()

    def centerWindow(self): 
        try:
            #set size
            w = 650
            h = 300
    
            sw = self.parent.winfo_screenwidth()
            sh = self.parent.winfo_screenheight()
            
            x = (sw - w)/2
            y = (sh - h)/2
            self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        except:
            self.parent.geometry("550x300+300+300")


def main():
  
    root = Tk()
    #root.geometry("550x300+300+300")
    app = Window(root)
    app.centerWindow()
    root.mainloop()  


if __name__ == '__main__':
    main()  