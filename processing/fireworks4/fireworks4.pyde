from random import randint
#from processing import *
from fireworks import Firework, DisplayManager
from displayList import getList

def setup():
    size(300,300)
    frameRate(24)  
    background(0) 
    stroke(255)
    strokeWeight(2)
    global display1
    
    display1 = DisplayManager()
    show = getList()                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                            
    for rocket in show:
        display1.addRocket(rocket[0],rocket[1])
                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def draw():
    background(0)
    display1.update()

def keyPressed():
    exit()
#The run() procedure below will call the setup() procedure followed by the draw() procedure.
#The draw() procedure will then be called 24 times per second (based on the frame rate set in the setup() procedure)
#run()