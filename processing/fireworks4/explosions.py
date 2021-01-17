from circle import getRandomPointInCircle, getRandomPointInCircleBand
from characters import explodingCharacter

def explosion(x,y,n,r):
    stroke(255,255,255)  
    sparkList = getRandomPointInCircle(x,y,n,r) 
    for spark in sparkList:
        point(spark[0],spark[1])
    
    stroke(255,0,255)        
    sparkList = getRandomPointInCircle(x,y,n,r+2) 
    for spark in sparkList:
        point(spark[0],spark[1])

def explosionBand(x,y,n,r):
    stroke(255,255,255)  
    sparkList = getRandomPointInCircleBand(x,y,n,r) 
    for spark in sparkList:
        point(spark[0],spark[1])
    
    stroke(255,0,255)        
    sparkList = getRandomPointInCircleBand(x,y,n,r+2) 
    for spark in sparkList:
        point(spark[0],spark[1])
        
def explodingCharacter(x,y,n,character='A'):
    sparkList = getRandomPointInLetter(x,y,n,character='A')
    for spark in sparkList:
        r=randint(0,255)
        g=randint(0,255)
        b=randint(0,255)
        stroke(r,g,b) 
        point(spark[0],spark[1])
    