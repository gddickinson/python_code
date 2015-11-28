# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 12:49:33 2015

@author: george
"""

import numpy as np
import random
import pylab
import math
import time



class Cell_no_Organelles(object):
    """
    Representation of a simplified 2D cell. 
    """    

    def __init__(self, width = 50, height = 50, startCa = 100, maxCa = 1000, rate = 1):
        """
        Initialization function, saves an array storing cell shape, calciumConc, ion channels

        startCa
        maxCa
        rate = rate at which calcium moves from one position to adjacent position every time step
        """

        self.cyto = np.zeros((width,height))
        self.startCa = startCa
        self.maxCa = maxCa
        self.rate = rate
        if self.startCa <= self.maxCa:        
            self.cyto = self.cyto + self.startCa
        else: self.cyto = self.cyto + self.maxCa

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

    def surroundingPositions(self, x,y):
        """
        returns valid coordiates in a cell for positions surrounding an x,y position
        """
        ans = []
        position = 8
                
        
        return ans




    def pointSourceCa(self, x, y, rate):
        """
        increases calciumConc at x,y position every time step according to rate
        """

        return      


    def pointSinkCa(self, x, y, rate):
        """
        decreases calciumConc at x,y position every time step according to rate
        """

        return  


    def update(self):
        """
        Update calciumCon for each position
        
        return array of positions and calciumConc
        """
        
         
        return self.cyto

