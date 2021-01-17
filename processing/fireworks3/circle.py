import math
from random import random


def getRandomPointInCircle(x, y, n, radius):
    ans = []
    for i in range (n):
        t = 2 * math.pi * random()
        u = random() + random()
        r = None
    
        if u > 1:
            r = 2 - u
        else:
            r = u
    
        resultX = radius * r * math.cos(t)
        resultY = radius * r * math.sin(t)
        
        ans.append([resultX+x,resultY+y])
    return ans

def getRandomPointInCircleBand(x, y, n, radius):
    ans = []
    for i in range (n*5):
        t = 2 * math.pi * random()
        u = random() + random()
        r = None
    
        if u > 1:
            r = 2 - u
        else:
            r = u
    
        resultX = radius * r * math.cos(t)
        resultY = radius * r * math.sin(t)
        
        distance = math.sqrt( ((0-resultX)**2)+((0-resultY)**2) )
        
        if (distance > (radius * 0.8)):
            ans.append([resultX+x,resultY+y])
    return ans