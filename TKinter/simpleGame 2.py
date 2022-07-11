# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 08:45:01 2016

@author: george
"""

from tkinter import *
from random import *


class game:
    def __init__(self):
        
        self.width = 500
        self.height = 500
        self.root=Tk()
        self.RUN=False
        
        self.frame=Frame(bg="black")
        self.frame.pack();
        
        self.canvas=Canvas(self.frame, bg="black",width = self.width,height = self.height)
        self.canvas.pack()
        
        self.clock=Label(self.frame, bg="black", fg="white")
        self.clock.pack()
        self.points=Label(self.frame, bg="black", fg="white")
        self.points.pack()
        self.button=Button(self.frame, bg="black", fg="white", text="Click to start",command=self.start)
        self.button.pack()
        
        self.root.mainloop()

    def start(self):
        self.time=0
        self.RUN=True
        
        #self.point=0
        
        self.x=100
        self.y=100
        self.tempx=100
        self.tempy=100
        self.UP=False
        self.DOWN=False
        self.LEFT=False
        self.RIGHT=False

        self.size=2
        self.canvas.bind("<ButtonPress-1>", self.onMClick)
        self.run()

    def paint(self):
        self.canvas.delete(ALL)

        if self.time//100<=60:
            if 10*self.size >0:
                ball=self.canvas.create_oval(self.x-10*self.size,self.y-10*self.size,self.x+10*self.size,self.y+10*self.size, fill="white")
            elif 10*self.size>150:
                self.clock['text']="You lost"
                self.end()
            else:
                self.clock['text']="You lost"
                self.end()
        else:
            self.clock['text']="Time's up"
            self.end()

    def onMClick(self,event):
        self.tempx=event.x
        self.tempy=event.y
        if event.x> self.x and self.x is not self.tempx :
            self.RIGHT=True
            self.LEFT=False
        elif event.x< self.x and self.x is not self.tempx :
            self.LEFT=True
            self.RIGHT=False
        else:
            self.x=self.tempx    
            self.RIGHT=False
            self.LEFT=False
        if event.y> self.y and self.y is not self.tempy :
            self.DOWN=True
            self.UP=False
        elif event.y< self.y and self.y is not self.tempy :
            self.UP=True
            self.DOWN=False
        else:
            self.y=self.tempy
            self.DOWN=False
            self.UP=False
    
    def move(self, b,speed):
            if self.UP==True and self.y-b>0:
                self.y-=speed
            elif self.UP==True and self.y-b<=0:
                self.UP=False
                self.DOWN=True
            if self.DOWN==True and self.y+b<self.height:
                self.y+=speed
            elif self.DOWN==True and self.y+b>=self.height:
                self.DOWN=False
                self.UP=True
            if self.LEFT==True and self.x-b>0:
                self.x-=speed
            elif self.LEFT==True and self.x-b<=0:
                self.LEFT=False
                self.RIGHT=True
            if self.RIGHT==True and self.x+b<self.width:
                self.x+=speed
            elif self.RIGHT==True and self.x+b>=self.width:
                self.RIGHT=False
                self.LEFT=True
    
    def run(self):
        if self.RUN is True:
            self.time+=1
            self.clock['text']="TIME:" + str(self.time//100)
            #self.points['text']="Points gathered: " + str(self.point)
            self.move(10*self.size,2)
            self.paint()
            self.root.after(10, self.run)
    
    def end(self):
        self.RUN=False
        self.canvas.unbind("<ButtonPress-1>")
 
app=game()