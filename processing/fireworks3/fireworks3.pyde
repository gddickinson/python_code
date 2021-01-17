from random import randint
#from processing import *
from fireworks import Firework


def setup():
    size(300,300)
    frameRate(24)  
    background(0) 
    stroke(255)
    strokeWeight(2)
    global fw
    fw = Firework() 

                
def draw():
    background(0)
    def keyPressed():
        #print('A key was pressed', keyboard.key)
        #exitp()
        exit()
    
    fw.display()

#The run() procedure below will call the setup() procedure followed by the draw() procedure.
#The draw() procedure will then be called 24 times per second (based on the frame rate set in the setup() procedure)
#run()