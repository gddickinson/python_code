from random import randint
from circle import getRandomPointInCircle, getRandomPointInCircleBand
from characters import getRandomPointInLetter, getRandomPointInJPG
import math
from particle_system import ParticleSystem

#mac
#pathName = '/Users/george/Desktop/text/'

#pc - google drive
pathName = 'C:\\Google Drive\\text\\'

class Firework(object):
    def __init__(self, singleColor=False, color=0, numberOfParticules=3, \
                      startPosition=0, setDirection=False, direction=0, directionLow=-2, directionHigh=2, setRocketVelocity = False, rocketVelocity = -8,\
                          setLifespan = True, life=20, repeat = True, delay=100, detonation = 50, flare = False, flareSize=20,\
                                  explosionsOn=True, setExplosionSize = False, explosionSize=30, explosionDuration = 15,\
                                      imageRocket = False, imageName = 'tree', characterRocket = False, character = "upper_A",\
                                          explosionTypeFlag=False, explosionType = 'firework'): 
 
        self.count = 0
        self.position = []       
        self.velocity = []
        self.life = life

        path = pathName + "sprite.png"
        sprite = loadImage(path)
        self.ps = ParticleSystem(100, sprite)
    
        self.imageRocket = imageRocket
        self.imageName = imageName
 
        self.flare = flare
        self.flareSize = flareSize
 
        self.setLifespan = setLifespan
        self.detonation = detonation
   
        self.detonated = False
         
        self.explosionTypeFlag = explosionTypeFlag
        self.explosionType = explosionType
        
        self.explosionDuration = explosionDuration     
                               
        self.repeat = repeat
        self.delay = delay

        self.dead = False
   
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
            
    def explosionBandDriftingDown(self,x,y,n,r):
        driftX = randint(-10,1)
        driftY = randint(0,1)        
        stroke(255,255,255)  

        sparkList = getRandomPointInCircleBand(x,y,n,r) 
        for spark in sparkList:
            point(spark[0]+driftX,spark[1]+driftY)
        
        stroke(255,0,255)        
        sparkList = getRandomPointInCircleBand(x,y,n/2,r+2) 
        for spark in sparkList:
            point(spark[0]+driftX,spark[1]+driftY)            

    def explodingCharacter(self,x,y,n,scaleFactor,character='upper_A'):
        sparkList = getRandomPointInLetter(x,y,n,scaleFactor,character)
        driftX = randint(-1,1)
        driftY = randint(0,1)
        for spark in sparkList:
            r=randint(0,255)
            g=randint(0,255)
            b=randint(0,255)
            stroke(r,g,b) 
            point(spark[0]+driftX,spark[1]+driftY)                                           
   
    def explodingImage(self,x,y,n,scaleFactor,imgName='tree'):
        sparkList = getRandomPointInJPG(x,y,n,scaleFactor,imgName)
        driftX = randint(-6,6)
        driftY = randint(-3,6)
        for spark in sparkList:
            r=randint(0,255)
            g=randint(0,255)
            b=randint(0,255)
            stroke(r,g,b) 
            point((spark[0] + driftX),(spark[1] + driftY))                                                                                                                                       

    def fakeParticle(self,x,y,n,scaleFactor,imgName='firework', sizeLimit=200):
        position = []
        velocity = []
        
        direction = randint(-15,15)
        sparkVelocity = randint(-20,20)
        
        position.append([x,y])
        velocity.append([direction, sparkVelocity])
                          
        for i in range(0, sizeLimit):
            newX = position[i][0]+velocity[i][0]
            newY = position[i][1]+velocity[i][1]   
            newX2 = position[i][0]-velocity[i][0]
            newY2 = position[i][1]-velocity[i][1]        
            position.append([newX,newY])
            position.append([newX2,newY2])           
            #Add Gravity
            newVelocity = velocity[i][1]+0.2
            velocity.append([velocity[i][0],newVelocity])
        
                
        for i in range(0,len(position)):
            r=randint(0,255)
            g=randint(0,255)
            b=randint(0,255)
            stroke(r,g,b) 
            distance = math.sqrt( ((x-position[i][0])**2)+((y-position[i][1])**2) )
            if (distance > 50):
                stroke(255,255,255)
            point((position[i][0]),(position[i][1])) 
                


    def getStatus(self):
        return self.dead        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    def display(self):
 
        displayNumber = self.count
 
        if (self.count < self.detonation):
 
            for i in range(0, self.numberOfParticules):
                #print(i)
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

                if (self.flare):
                    self.explosion(self.position[displayNumber+i][0] + 150,self.position[displayNumber+i][1] +300, randint(0,10),randint(0,(self.flareSize/((i+1)*2))))


        else:
                    
            if (self.explosionDuration+self.detonation > self.count):
                        
                if self.detonated == False:
                    self.ps.init(self.position[displayNumber+self.numberOfParticules][0] + 150,self.position[displayNumber+self.numberOfParticules][1] +300) 
                    self.detonated = True
                
                if (self.explosionTypeFlag):
                    #self.fakeParticle(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,500),1,imgName=self.explosionType)
                    
                    if self.detonated == False:
                        self.ps.setEmitter(self.position[displayNumber+self.numberOfParticules][0] + 150,self.position[displayNumber+self.numberOfParticules][1] +300)    
                    self.ps.update()
                    self.ps.display()
                    

                    
                else:    
                    if (self.explosionsOn):
                        if randint(0,100)>50:
                            self.explosionBandDriftingDown(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,20),randint(0,self.explosionSize+1))
                        self.explosion(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,20),randint(0,self.explosionSize))
                        if randint(0,100)>50:
                            self.explosionBand(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,20),randint(0,self.explosionSize+10))                                    
    
                    if (self.characterRocket):
                        self.explodingCharacter(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,20),self.scaleFactor,character=self.character)
        
                    if (self.imageRocket):                    
                        #self.ps.setEmitter(self.position[displayNumber+self.numberOfParticules][0] + 150,self.position[displayNumber+self.numberOfParticules][1] +300)
                        #self.ps.update()
                        #self.ps.display()
                        
                        self.explodingImage(self.position[displayNumber][0] + 150,self.position[displayNumber][1] +300, randint(0,500),10,imgName=self.imageName)

        self.count +=1
        
        if (self.repeat):
            if (self.count > self.life + self.delay):
                self.count = 0
        else:
            if (self.count > self.life + self.delay):
                self.dead = True     

class DisplayManager(object):
    def __init__(self):
        self.count = 0        
        self.displayList = []
        
    def addRocket(self, rocket, startTime):
        self.displayList.append([rocket,startTime])    

    def display(self):
       for i in range(0,len(self.displayList)):
           if (self.displayList[i][1] <= self.count):
               self.displayList[i][0].display()     
           
           if (self.displayList[i][0].getStatus == False):
               del self.displayList[i]
                
             
               
    def update(self):
        self.count +=1
        self.display()
        #print(self.count)
        pass
        
        
        