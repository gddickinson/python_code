# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 08:45:01 2016

@author: george
"""

from tkinter import *
from random import *
import numpy as np


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
        self.forward = Button(self.frame, bg="black", fg="white", text="Forward",command=self.forward)
        self.forward.pack()
        self.rotateLeft = Button(self.frame, bg="black", fg="white", text="Rotate Left",command=self.rotateLeft)
        self.rotateLeft.pack(side=LEFT)
        self.rotateRight = Button(self.frame, bg="black", fg="white", text="Rotate Right",command=self.rotateRight)
        self.rotateRight.pack(side=RIGHT)
        self.button=Button(self.frame, bg="black", fg="white", text="Click to start",command=self.start)
        self.button.pack()
        self.reverse = Button(self.frame, bg="black", fg="white", text="Reverse",command=self.reverse)
        self.reverse.pack()
        
        self.root.mainloop()

    def start(self):
        self.time=0
        self.RUN=True
        
        #self.point=0        
        self.x=100.0
        self.y=100.0
        self.x1 = self.x
        self.x2 = self.x + 5
        self.x3 = self.x - 5

        self.y1 = self.y + 10
        self.y2 = self.y - 10
        self.y3 = self.y - 10
        
        self.rotation = 0.0
        self.targetx=100.0
        self.targety=100.0

        self.size=1
        self.canvas.bind("<ButtonPress-1>", self.onMClick)
        self.run()


    def forward(self):
        differenceX = self.x1 - self.x
        differenceY = self.y1 - self.y      
        
        self.x = self.x1
        self.y = self.y1
        self.x1 = self.x1 + differenceX
        self.x2 = self.x2 + differenceX
        self.x3 = self.x3 + differenceX
        self.y1 = self.y1 + differenceY
        self.y2 = self.y2 + differenceY
        self.y3 = self.y3 + differenceY

    def reverse(self):
        differenceX = self.x1 - self.x
        differenceY = self.y1 - self.y      
        
        self.x = self.x - differenceX
        self.y = self.y - differenceY
        self.x1 = self.x1 - differenceX
        self.x2 = self.x2 - differenceX
        self.x3 = self.x3 - differenceX
        self.y1 = self.y1 - differenceY
        self.y2 = self.y2 - differenceY
        self.y3 = self.y3 - differenceY
                    
    def rotateRight(self):
        self.rotation += 10
        
    def rotateLeft(self):
        self.rotation -= 10

    def paint(self):
        self.canvas.delete(ALL)

        if self.time//100<=60:
            if 10*self.size >0:
                robot=self.canvas.create_polygon(self.x1*self.size,self.y1*self.size,self.x2*self.size,self.y2*self.size, self.x3*self.size,self.y3*self.size, fill="white")

                target=self.canvas.create_oval(self.targetx-10*self.size,self.targety-10*self.size,self.targetx+10*self.size,self.targety+10*self.size, fill="red")

        else:
            self.clock['text']="Time's up"
            self.end()

    def onMClick(self,event):
        self.targetx=event.x
        self.targety=event.y

    def rotatePoint(self,centerPoint,point,angle):
        """Rotates a point around another centerPoint. Angle is in degrees.
        Rotation is counter-clockwise"""
        angle = math.radians(angle)
        temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
        temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
        temp_point1 = temp_point[0]+centerPoint[0]
        temp_point2 = temp_point[1]+centerPoint[1]
        return temp_point1, temp_point2

    
    def move(self, b,speed):
        #return
        ###rotation###

        self.x1, self.y1 = self.rotatePoint((self.x,self.y),(self.x1,self.y1), self.rotation)        
        self.x2, self.y2 = self.rotatePoint((self.x,self.y),(self.x2,self.y2), self.rotation)
        self.x3, self.y3 = self.rotatePoint((self.x,self.y),(self.x3,self.y3), self.rotation)
        
        self.rotation = 0.0

                
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