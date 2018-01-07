from random import randint
from circle import getRandomPointInCircle, getRandomPointInCircleBand
from characters import getRandomPointInLetter, getRandomPointInJPG

class Firework(object):
    def __init__(self, singleColor=False, color=0, numberOfParticules=3, \
                      startPosition=0, setDirection=False, direction=0, directionLow=-2, directionHigh=2, setRocketVelocity = False, rocketVelocity = -8,\
                          setLifespan = True, life=20, repeat = True, delay=100, detonation = 50,\
                                  explosionsOn=True, setExplosionSize = False, explosionSize=30, explosionDuration = 15,\
                                      characterRocket = False, character = "upper_A"): 
 
        self.count = 0
        self.position = []       
        self.velocity = []
        self.life = life
 
        self.setLifespan = setLifespan
        self.detonation = detonation
    
        self.explosionDuration = explosionDuration     
                               
        self.repeat = repeat
        self.delay = delay
 
        self.characterRocket = characterRocket
        if self.characterRocket == True:
            self.character = character
             
        self.setRocketVelocity = setRocketVelocity
        if self.setRocketVelocity:
            self.rocketVelocity = rocketVelocity
        else:
            self.rocketVelocity = randint(-10,-5)
        
        self.scaleFactor = randint(5,15)    
                                                                                                                                                                                                           
        self.numberOfParticules = numberOfParticules
        self.explosionsOn = explosionsOn
        self.setExplosionSize = setExplosionSize 
        if (self.setExplosionSize == True):
            self.explosionSize = explosionSize
        else:
            self.explosionSize = randint(0,100)
     
        self.singleColor = singleColor
        if (self.singleColor):
            self.color= color
        else:
            self.color = 0
                
        self.setDirection = setDirection
        self.directionLow = directionLow
        self.directionHigh = directionHigh      
        if (self.setDirection == True):
            self.direction = direction
        else:
            self.direction = randint(self.directionLow,self.directionHigh)    
 
                      
        self.startPosition = startPosition


        def makeTrajectory(self): 
            self.position.append([self.startPosition,0])
            self.velocity.append([self.direction, self.rocketVelocity])
                          
            for i in range(0, 300):
                newX = self.position[i][0]+self.velocity[i][0]
                newY = self.position[i][1]+self.velocity[i][1]          
                self.position.append([newX,newY])
                #Add Gravity
                newVelocity = self.velocity[i][1]+0.2
                self.velocity.append([self.velocity[i][0],newVelocity])
                 
        makeTrajectory(self)                                   
                                                                
                                                                                                          
    def explosion(self,x,y,n,r):
        stroke(255,255,255)  
        sparkList = getRandomPointInCircle(x,y,n,r) 
        for spark in sparkList:
            point(spark[0],spark[1])
        
        stroke(255,0,255)        
        sparkList = getRandomPointInCircle(x,y,n,r+2) 
        for spark in sparkList:
            point(spark[0],spark[1])
  
    def explosionBand(self,x,y,n,r):
        stroke(255,255,255)  
        sparkList = getRandomPointInCircleBand(x,y,n,r) 
        for spark in sparkList:
            point(spark[0],spark[1])
        
        stroke(255,0,255)        
        sparkList = getRandomPointInCircleBand(x,y,n,r+2) 
        for spark in sparkList:
            point(spark[0],spark[1])    

    def explodingCharacter(self,x,y,n,scaleFactor,character='upper_A'):
        sparkList = getRandomPointInLetter(x,y,n,scaleFactor,character)
        for spark in sparkList:
            r=randint(0,255)
            g=randint(0,255)
            b=randint(0,255)
            stroke(r,g,b) 
            point(spark[0],spark[1])                                           
   
    def explodingImage(self,x,y,n,scaleFactor,imgName='tree'):
        sparkList = getRandomPointInJPG(x,y,n,scaleFactor,imgName)
        for spark in sparkList:
            r=randint(0,255)
            g=randint(0,255)
            b=randint(0,255)
            stroke(r,g,b) 
            point(spark[0],spark[1])                                                                                                                                       
                                                                                                                                                                                                                                                                                                                                                                                                      
                                                                                                                            
    def display(self):
 
        displayNumber = self.count
 
        if (self.count < self.detonation):
 
            for i in range(0, self.numberOfParticules):
                if (self.singleColor == False):
                    self.color=i%5
                if self.color==0:
                    stroke(255,255,255)    
                elif self.color==1:
                    stroke(255,255,0)
                elif self.color==2:
                    stroke(255,0,255)
                elif self.color==3:
                    stroke(0,255,0)
                elif self.color==4:
                    stroke(0,255,255)
                                    
                point(self.position[displayNumber+i][0] + 150, self.position[displayNumber+i][1] + 300)

        else:
            if (self.explosionDuration+self.detonation > self.count):
                if (self.explosionsOn):
                    self.explosionBand(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,20),randint(0,self.explosionSize+1))
                    self.explosion(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,20),randint(0,self.explosionSize))

                if (self.characterRocket):
                    self.explodingCharacter(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,20),self.scaleFactor,character=self.character)
                    #self.explodingImage(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,20),5,imgName="tree")

        self.count +=1
        
        if (self.repeat):
            if (self.count > self.life + self.delay):
                self.count = 0


class DisplayManager(object):
    def __init__(self):
        pass