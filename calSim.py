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



class Cell_no_Organelles(object):
    """
    Representation of a simplified 2D cell. 
    """    

    def __init__(self, width = 100, height = 100, startCa = 100, maxCa = 2000, rate = 1):
        """
        Initialization function, saves an array storing cell shape, calciumConc, ion channels

        startCa
        maxCa
        rate = rate at which calcium moves from one position to adjacent position every time step
        """

        self.cyto = np.zeros((width,height))
        self.width = width
        self.height = height
        self.startCa = startCa
        self.maxCa = maxCa
        self.rate = rate
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
        addCa to a position in cyto
        """

        if self.cyto[x][y] - calciumConc >= 0:        
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
        
        for i in range(len(randomXY)):
            self.setBorderCa(100)
            surroundingCa = 0
            testXYCa = self.cyto[randomXY[i][0]][randomXY[i][1]]
            surroundingXY = self.getSurroundingPositions(randomXY[i][0],randomXY[i][1])
            for j in range(len(surroundingXY)):
                surroundingCa += self.cyto[surroundingXY[j][0]][surroundingXY[j][1]]
            totalCa = testXYCa + surroundingCa
            averageCa = float(totalCa)/float(len(surroundingXY)+1)
            for j in range(len(surroundingXY)):
                self.setCa(surroundingXY[j][0],surroundingXY[j][1], averageCa)           
        return self.cyto

  
        
    
test = Cell_no_Organelles()
test.setCa(25,25,500)
#test.setCa(55,55,1000)
fig = plt.figure()
#==============================================================================
# movie = [(test.getCytoCa())]
# for i in range(30):   
#     test.update_mean()
#     movie = movie + [(test.getCytoCa())]
# plt.imshow(test.cyto)
#==============================================================================

im = plt.imshow(test.update_mean(), animated=True)

def runSim(*args):
    print(args)
    if args == (5,):
        test.setCa(40,40,500)
    if args == (20,):
        test.setCa(25,25,1000)        
    
    im.set_array(test.update_mean())
    return im,

ani = animation.FuncAnimation(fig, runSim, frames= 50,interval=50, blit=True)
plt.show()