from random import randint


class Firework(object):
    def __init__(self, singleColor=True, color=0, numberOfParticules=10, \
                      startPosition=0, setDirection=False, direction=0, directionLow=-2, directionHigh=2, \
                          setLifespan = True, life=40, \
                              limitedTime = False, duration=100, \
                                  explosionsOn=True, setExplosionSize = False, explosionSize=30, minHeight = 280): 
 
        self.position = []       
        self.velocity = []
        self.lifespan = life
        self.rocketColor = []
     
        self.rocketVelocity = randint(-10,-5)
                                                                                                        
        self.minHeight = minHeight    
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
 
        self.setLifespan = setLifespan
        if (self.setLifespan):
            self.life = life
            self.lifeFinal = life + randint(0,20)
        else:
            self.life = randint(0,40)
            self.lifeFinal = randint(20,40)   
                      
        self.startPosition = startPosition

            
        def addToLaunch(self, particules):                
            for i in range(0, particules):
                self.position.append([self.startPosition,0])
                self.velocity.append([self.direction, self.rocketVelocity])
                self.rocketColor.append(self.color)

              
        addToLaunch(self, self.numberOfParticules)

    
    def update(self):        
        for i in range(0, self.numberOfParticules):
            self.position[i][0]+=self.velocity[i][0]
            self.position[i][1]+=self.velocity[i][1]
            #Add Gravity
            self.velocity[i][1]+=0.2
        self.lifespan -=1
        #print(self.lifespan)
        if (self.lifespan < 0): 
            self.color = 10
            return
 
                      
    def display(self):
        if (self.color == 10):
            stroke(0,0,0)
 
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
                        
            point(self.position[i][0] + 150, self.position[i][1] + 300)
        
        self.update()
        
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

            print(self.position)
            point(self.position[i][0] + 150, self.position[i][1] + 300)
        

class DisplayManager(object):
    def __init__(self):
        pass