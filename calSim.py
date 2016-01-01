# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 12:49:33 2015

@author: george
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import math
import time
import matplotlib.animation as animation
import cv2

#==============================================================================
# filename = '/home/george/Pictures/shakespeare.jpg'
# img = cv2.imread(filename,0)/100
# height = size(img,1)
# width = size(img,0)
#==============================================================================

class Cell_no_Organelles(object):
    """
    Representation of a simplified 2D cell. 
    """    

    def __init__(self, width = 100, height = 100, startCa = 100, maxCa = 1000, backgroundImg=[], channelList =[], pumpList=[]):
        """
        Initialization function, saves an array storing cell shape, calciumConc, ion channels

        startCa
        maxCa
        rate = rate at which calcium moves from one position to adjacent position every time step
        """

        self.cyto = np.zeros((width,height))
        self.backgroundImg = backgroundImg
        self.width = width
        self.height = height
        self.startCa = startCa
        self.maxCa = maxCa
        self.channelList = channelList
        self.pumpList = pumpList
        if self.startCa <= self.maxCa:        
            self.cyto = self.cyto + self.startCa
        else: self.cyto = self.cyto + self.maxCa

    def setCa(self, x, y, calciumConc):
        """
        addCa to a position in cyto
        """        
        if calciumConc <= self.maxCa:        
            self.cyto[x][y] = calciumConc 
        else:
            self.cyto[x][y] = self.maxCa
        return 

    def addChannels (self, channelList, pumpList):
        self.channelList = self.channelList + channelList
        self.pumpList = self.pumpList + pumpList
        return

    def getChannels(self):
        ans = []
        for channel in self.channelList:
            ans.append((channel.getX(),channel.getY(),channel.stateOpen, self.getCa(channel.getX(),channel.getY())))
        return ans

    def getPumps(self):
        ans = []
        for pump in self.pumpList:
            ans.append((pump.getX(),pump.getY(),pump.stateOpen, self.getCa(pump.getX(),pump.getY())))
        return ans


    def getCa(self, x, y):
        """
        Returns the [calcium] for a position in cyto
        """
        return self.cyto[x][y]


    def addCa(self, x, y, calciumConc):
        """
        addCa to a position in cyto
        """

        if self.cyto[x][y] + calciumConc <= self.maxCa:        
            self.cyto[x][y] = self.cyto[x][y] + calciumConc 
        else:
            self.cyto[x][y] = self.maxCa
        return 

    def subtractCa(self, x, y, calciumConc):
        """
        subtract Ca from a position in cyto
        """

        if self.cyto[x][y] - calciumConc > 0:        
            self.cyto[x][y] = self.cyto[x][y] - calciumConc 
        else:
            self.cyto[x][y] = 0
        return

    def getTotalCa(self):
        return np.sum(self.cyto)

    def getSurroundingPositions(self, x,y):
        """
        returns valid coordiates in a rectangular cell surrounding one x,y position
        """
        
        if x == 0:
            if y == 0:
                return [(x,y+1),(x+1,y+1),(x+1,y)]
            if y < self.height and y > 0:
                return [(x,y+1), (x,y-1), (x+1,y+1), (x+1,y), (x+1,y-1)]
            if y == self.height:
                return [(x,y-1), (x+1,y), (x+1,y-1)]

        if y == 0:
            if x < self.width and x > 0:
                return [(x+1,y), (x-1,y), (x+1,y+1), (x,y+1), (x-1,y+1)]
            if x == self.width:
                return [(x-1,y), (x,y+1), (x-1,y+1)]

        if x == self.width:
            if y == self.height:
                return [(x, y-1), (x-1,y), (x-1,y-1)]
            if y < self.width and y > 0:                
                return [(x-1,y), (x-1,y-1), (x, y-1), (x+1,y), (x+1,y+1)]            

            
        return [(x-1,y+1), (x,y+1), (x+1, y+1), (x-1,y), (x+1,y), (x-1,y-1), (x, y-1), (x+1,y-1)]


    def getSurroundingPositionsWithLowerCa(self, x, y):
        ans = []
        calciumConc = self.cyto[x][y]
        positions = self.getSurroundingPositions(x,y)
        for xy in positions:
            if self.cyto[xy[0]][xy[1]] < calciumConc:
                ans.append(xy)
        return ans
            
    def getCytoCa(self):
        return self.cyto

    def randomListXY(self):
        """
        returns list of positions in cell in random order
        """
        ans = []
        x = range(0, self.width-1)
        #random.shuffle(x)
        y = range(0, self.height-1)
        #random.shuffle(y)
        for i in range(len(x)):
            for j in range(len(y)):
                ans.append((x[i],y[j]))
        random.shuffle(ans)
        return ans

    def setBorderCa(self, calciumConc):
        self.cyto[0] = calciumConc
        self.cyto[-1] = calciumConc
        self.cyto[:,0] = calciumConc
        self.cyto[:,-1] = calciumConc
        return

    def update_mean(self):
        """
        Update calciumCon for each position
        
        return array of positions and calciumConc
        """
        randomXY = self.randomListXY()

        for channel in self.channelList:
            self.addCa(channel.getX(),channel.getY(),channel.amountOfCaThisTime())
 
        for pump in self.pumpList:
            self.subtractCa(pump.getX(),pump.getY(),pump.amountOfCaThisTime())
       
        for i in range(len(randomXY)):
            self.setBorderCa(self.startCa)
            surroundingCa = 0
            testXYCa = self.cyto[randomXY[i][0]][randomXY[i][1]]
            surroundingXY = self.getSurroundingPositions(randomXY[i][0],randomXY[i][1])
            for j in range(len(surroundingXY)):
                surroundingCa += self.cyto[surroundingXY[j][0]][surroundingXY[j][1]]
            totalCa = testXYCa + surroundingCa
            averageCa = float(totalCa)/float(len(surroundingXY)+1)
            for j in range(len(surroundingXY)):
                self.setCa(surroundingXY[j][0],surroundingXY[j][1], averageCa)           
        
        if self.backgroundImg != []:
            self.cyto = self.backgroundImg + self.cyto

        return self.cyto

class Channel(object):
    """
    Representation of a basic calcium sensitive channel. 
    """    

    def __init__(self, x, y, cell, activatingCa = 110, inactivatingCa = 130, conductance=600):
        """
        Initializes a position with coordinates (x, y) in cell object
        """
        self.x = x  
        self.y = y
        self.cell = cell
        self.activatingCa = activatingCa
        self.inactivatingCa = inactivatingCa
        self.conductance = conductance
        self.stateOpen = False
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y    
    
    def updateActiveState(self):
        xyCalcium = self.cell.getCa(self.getX(),self.getY())
        if xyCalcium > self.activatingCa and xyCalcium < self.inactivatingCa:
            chanceOfActivation = ((xyCalcium-self.activatingCa)/(self.inactivatingCa-self.activatingCa))
            if random.random() > chanceOfActivation:
                print chanceOfActivation
                self.stateOpen = True
        else:
            self.stateOpen = False
        return

    def amountOfCaThisTime(self):
        self.updateActiveState()
        if self.stateOpen == False:
            return 0
        return self.conductance

class Pump(object):
    """
    Representation of a basic calcium sensitive channel. 
    """    

    def __init__(self, x, y, cell, activatingCa = 130, inactivatingCa = 10000, conductance=1000):
        """
        Initializes a position with coordinates (x, y) in cell object
        """
        self.x = x  
        self.y = y
        self.cell = cell
        self.activatingCa = activatingCa
        self.inactivatingCa = inactivatingCa
        self.conductance = conductance
        self.stateOpen = False
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y    
    
    def updateActiveState(self):
        xyCalcium = self.cell.getCa(self.getX(),self.getY())
        if xyCalcium > self.activatingCa:
            chanceOfActivation = ((xyCalcium-self.activatingCa)/(self.inactivatingCa-self.activatingCa))
            if random.random() > chanceOfActivation:
                print chanceOfActivation
                self.stateOpen = True
        else:
            self.stateOpen = False
        return

    def amountOfCaThisTime(self):
        self.updateActiveState()
        if self.stateOpen == False:
            return 0
        return self.conductance

    
test = Cell_no_Organelles(width = 100, height = 100, startCa = 100, maxCa = 2000)

channel1 = Channel(30,30, test)
channel2 = Channel(40,40, test)
channel3 = Channel(50,50, test)
channel4 = Channel(31,31, test)
channel5 = Channel(32,32, test)
channel6 = Channel(30,31, test)


#pump1 = Pump(40,40, test)
#pump2 = Pump(40,41, test)
#pump3 = Pump(40,42, test)
#pump4 = Pump(40,43, test)
#pump5 = Pump(41,40, test)
#pump6 = Pump(41,41, test)
#pump7 = Pump(41,42, test)
#pump8 = Pump(41,43, test)

pumpList = []
for x in range(0,100,10):
    for y in range (0,100,10):
        pumpList.append(Pump(x,y,test))


channelList= [channel1,channel2,channel3, channel4, channel5, channel6]
#pumpList =[pump1, pump2, pump3, pump4, pump5, pump6, pump7, pump8]
test.addChannels(channelList, pumpList)

test.setCa(29,29,2000)
#test.setCa(55,55,1000)
fig = plt.figure()

im = plt.imshow(test.update_mean(), animated=True)

def runSim(*args):
    x = random.randint(0,width)
    y = random.randint(0,height)
    amount = random.randint(1,1000)
    z1 = random.randint(0,50)
    z2 = random.randint(0,50)
    z3 = random.randint(0,50)
    print(args)
    if args == (z1,):
        test.addCa(x,y,amount)
    if args == (z2,):
        test.addCa(x,y,amount)        
    if args == (z3,):
        test.addCa(x,y,amount)      
    im.set_array(test.update_mean())
    return im,

def runSim2(*args):
    print(args)
    print(test.getPumps())
    im.set_array(test.update_mean())
    return im,


if __name__ == '__main__':

    ani = animation.FuncAnimation(fig, runSim2, frames= 50,interval=50, blit=True)
    plt.show(ani)