from random import randint
#from processing import *
from fireworks import Firework

def setup():
    size(300,300)
    frameRate(24)  
    background(0) 
    stroke(255)
    strokeWeight(2)
    global fwa, fwb, fw1, fw2, fw3, fw4, fw5
    fwa = Firework(setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=50, explosionDuration = 5, setDirection=True, direction=1) 
    fw1 = Firework(startPosition=-90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 15, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "upper_H") 
    fw2 = Firework(startPosition=-45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "A") 
    fw3 = Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "P") 
    fw4 = Firework(startPosition=45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "P") 
    fw5 = Firework(startPosition=90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "Y") 
                
def draw():
    background(0)
    
    fwa.display()
    fw1.display()
    fw2.display()    
    fw3.display()    
    fw4.display()    
    fw5.display() 

def keyPressed():
    exit()
#The run() procedure below will call the setup() procedure followed by the draw() procedure.
#The draw() procedure will then be called 24 times per second (based on the frame rate set in the setup() procedure)
#run()