# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 18:44:58 2015

@author: george
"""

import pylab

class Location(object):
    
    def __init__(self, x, y):
        """x and y are floats"""
        self.x = x
        self.y = y
        
    def move(self, deltaX, deltaY):
        """deltaX and deltaY are floats"""
        return Location(self.x + deltaX, self.y + deltaY)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def distFrom(self, other):
        ox = other.x
        oy = other.y
        xDist = self.x - ox
        yDist = self.y - oy
        return (xDist**2 + yDist**2)**0.5
    
    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'





class Field(object):
    
    def __init__(self):
        self.drunks = {}
        
    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc
            
    def moveDrunk(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        #use move method of Location to get new location
        self.drunks[drunk] = currentLocation.move(xDist, yDist)
        
    def getLoc(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


import random


class Drunk(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'This drunk is named ' + self.name
    
class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0,1.0), (0.0,-1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)

class PolarBearDrunk(Drunk):
    def takeStep(self):
       directionList = [(0.0, 0.5), (1.0, 0.0), (-1.0, 0.0), (0.0, -1.5)]
       return random.choice(directionList)

class ColdDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0,0.9), (0.0,-1.03), (1.03, 0.0), (-1.03, 0.0)]
        return random.choice(stepChoices)

class EDrunk(Drunk):
    def takeStep(self):
        ang = 2 * math.pi * random.random()
        length = 0.5 + 0.5 * random.random()
        return (length * math.sin(ang), length * math.cos(ang))

class PhotoDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
                    [(0.0, 0.5),(0.0, -0.5),
                     (1.5, 0.0),(-1.5, 0.0)]
        return random.choice(stepChoices)

class DDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
                    [(0.85, 0.85), (-0.85, -0.85),
                     (-0.56, 0.56), (0.56, -0.56)] 
        return random.choice(stepChoices)


def walk(f, d, numSteps):
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return(start.distFrom(f.getLoc(d)))

def walkVector(f, d, numSteps):
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return(f.getLoc(d).getX() - start.getX(),
           f.getLoc(d).getY() - start.getY())


def simWalks(numSteps, numTrials):
    homer = UsualDrunk('Homer')
    notOrigin = Location(1, 0)
    distances = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(homer, notOrigin)
        distances.append(walk(f, homer, numTrials))
    return distances

def drunkTest(numTrials = 20):
    for numSteps in [10, 100, 1000, 10000]:
        distances = simWalks(numSteps, numTrials)
        print 'Random walk of ' + str(numSteps) + ' steps'
        print ' Mean =', sum(distances)/len(distances)
        print ' Max =', max(distances), 'Min =', min(distances)

def simulation(drunk = UsualDrunk('Usual')):
    test = Field()
    start = Location(0,0)
    
    test.addDrunk(drunk, start)
    
    x = []
    y = []
    for i in range(10000):
        print i
        test.moveDrunk(drunk)
        x.append(test.getLoc(drunk).getX())
        y.append(test.getLoc(drunk).getY())
    return x,y


    
#x,y = simulation(drunk = UsualDrunk('Usual'))
#x,y = simulation(drunk = PolarBearDrunk('PolarBear'))
#x,y = simulation(drunk = ColdDrunk('Cold'))
#x,y = simulation(drunk = EDrunk('EDrunk'))
#x,y = simulation(drunk = PhotoDrunk('PhotoDrunk'))
#x,y = simulation(drunk = DDrunk('DDrunk'))

x,y = simulation2()

pylab.scatter(x,y)


