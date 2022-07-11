# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 18:30:40 2015

@author: robot
"""

import pylab
import random

def montyChoose(guessDoor, prizeDoor1, prizeDoor2):
    if 1 != guessDoor and 1 != prizeDoor1 and 1!= prizeDoor2:
        return 1
    if 2 != guessDoor and 2 != prizeDoor1 and 2 != prizeDoor2:
        return 2
    if 3 != guessDoor and 3 != prizeDoor1 and 3 != prizeDoor2:
        return 3
    return 4

#==============================================================================
# def randomChoose(guessDoor, prizeDoor):
#     if guessDoor == 1:
#         return random.choice([2,3])
#     if guessDoor == 2:
#         return random.choice([1,3])
#     return random.choice([1,2])
#==============================================================================
    
def simMontyHall(numTrials, chooseFcn):
    stickWins, switchWins, noWin = (0, 0, 0)
    prizeDoorChoices = [1,2,3,4]
    guessChoices = [1,2,3,4]
    for t in range(numTrials):
        prizeDoor1 = random.choice([1, 2, 3, 4])
        prizeDoor2 = 0
        while prizeDoor2 == 0:
            prizeDoor2 = random.choice([1, 2, 3, 4])
            if prizeDoor2 == prizeDoor1:
                prizeDoor2 = 0
        guess = random.choice([1, 2, 3, 4])
        toOpen = chooseFcn(guess, prizeDoor1, prizeDoor2)
        if toOpen == prizeDoor1 or toOpen == prizeDoor2:
            noWin += 1
        elif guess == prizeDoor1 or guess == prizeDoor2:
            stickWins += 1
        else:
            switchWins += 1
    return (stickWins, switchWins)

def displayMHSim(simResults, title):
    stickWins, switchWins = simResults
    pylab.pie([stickWins, switchWins],
              colors = ['r', 'c'],
              labels = ['stick', 'change'],
              autopct = '%.2f%%')
    pylab.title(title)

simResults = simMontyHall(1000000, montyChoose)
displayMHSim(simResults, 'Monty Chooses a Door')
pylab.figure()
#simResults = simMontyHall(100000, randomChoose)
#displayMHSim(simResults, 'Door Chosen at Random')
pylab.show()