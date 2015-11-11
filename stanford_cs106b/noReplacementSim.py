# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 20:46:22 2015

@author: robot
"""
import random


def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    

    def allthesame(numberRed, numberGreen, numberDrawn):
        
        
        bucket = []
        draw = []
        for i in range(numberRed):
            bucket.append('r')
        for i in range(numberGreen):
            bucket.append('g')

        for i in range(numberDrawn):
            draw.append(bucket.pop(random.randint(0,len(bucket)-1)))

        #print(draw)            
        try:
            for i in range(len(draw)):
                if draw[i] != draw[i+1]:
                    return False
        except:                    
            return True
        
    numberTheSame = 0
    for i in range(numTrials):
        if allthesame(3,3,3) == True:
            numberTheSame +=1

    #print(numberTheSame,numTrials)
    return (float(numberTheSame)/float(numTrials))    

numTrials = 100000
print(noReplacementSimulation(numTrials))    