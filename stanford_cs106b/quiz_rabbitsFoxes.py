# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 17:01:24 2015

@author: george
"""

import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP
    
    probabilityRabbit = (1.0-(float(CURRENTRABBITPOP)/float(MAXRABBITPOP)))
    numberOfNewRabbits = 0
    for i in range(CURRENTRABBITPOP):
        chance = random.random()
        if chance <= probabilityRabbit:
            numberOfNewRabbits +=1
    newRabbitPop = CURRENTRABBITPOP + numberOfNewRabbits
    
    if newRabbitPop < 10:
        CURRENTRABBITPOP = 10
        return
    
    if newRabbitPop > MAXRABBITPOP:
        CURRENTRABBITPOP = MAXRABBITPOP
        return
    
    CURRENTRABBITPOP = newRabbitPop
            
    return
            
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP

    probabilityRabbitEaten = (float(CURRENTRABBITPOP)/float(MAXRABBITPOP))
    rabbitsEaten = 0

    for i in range(CURRENTFOXPOP):
        chance = random.random()
        if chance < probabilityRabbitEaten:
            rabbitsEaten +=1
    
    if CURRENTRABBITPOP - rabbitsEaten <10:
        CURRENTRABBITPOP = 10

    else:
        CURRENTRABBITPOP = CURRENTRABBITPOP - rabbitsEaten

    foxesBorn = 0

    for i in range(rabbitsEaten):
        chance = random.random()
        if chance < 0.333333:
            foxesBorn +=1 

    CURRENTFOXPOP =  CURRENTFOXPOP + foxesBorn
    if CURRENTFOXPOP > 1000:
        CURRENTFOXPOP = 1000

    foxesDied = 0
  
    for i in range(CURRENTFOXPOP -(2*foxesBorn)):
        chance = random.random()
        if chance < 0.1:
            foxesDied += 1

    if CURRENTFOXPOP <=10:
        return

    elif CURRENTFOXPOP - foxesDied < 10:
        CURRENTFOXPOP = 10

    else:
        CURRENTFOXPOP = CURRENTFOXPOP - foxesDied
    
    return
    
            
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """

    rabbit_populations = []
    fox_populations = []
    
    for i in range(numSteps):
        rabbitGrowth()
        foxGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP)


    return (rabbit_populations,fox_populations)


#==============================================================================
x = runSimulation(200)
timeSteps = []
time = 0
for i in range(len(x[0])):
    time +=1
    timeSteps.append(time)
    

pylab.plot(timeSteps,x[1], 'red')
pylab.plot(timeSteps,x[0])
#==============================================================================
coeff = polyfit(range(len(rabbitPopulationOverTime)), rabbitPopulationOverTime, 2)