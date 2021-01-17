from circle import getRandomPointInCircle, getRandomPointInCircleBand

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