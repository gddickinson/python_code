# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials=1):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    def simulationWithDrug(numViruses=100, maxPop=1000, maxBirthProb=0.1, clearProb=0.05, resistances= {'guttagonol': False},
                           mutProb=0.005, numTrials=1, timeDrugAdded=0):

        runTime = timeDrugAdded+150
        virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
        virusList = []    
        for i in range(numViruses):
            virusList.append(virus)
        
        trialResults = [0.0] * runTime
        resistantViruses = [0.0] * runTime
        for i in range (numTrials):
            patient = TreatedPatient(virusList,maxPop)
            totalVirusPop = []
            resistantVirusPop = []
            for x in range(runTime):
                if x >= timeDrugAdded:
                    patient.addPrescription('guttagonol')
                totalVirusPop.append(float(patient.update()))
                resistantVirusPop.append(float(patient.getResistPop(['guttagonol'])))
                
            for i in range(len(totalVirusPop)):
                trialResults[i] = float(trialResults[i])+float(totalVirusPop[i])
                resistantViruses[i] = float(resistantViruses[i]) + float(resistantVirusPop[i])               
    

        return totalVirusPop, resistantVirusPop


    totalPop, resistantPop = simulationWithDrug()

    pylab.hist(totalPop)
    pylab.xlabel('Total virus population')
    pylab.ylabel('Number of Trials')
    pylab.legend()
    pylab.show()



simulationDelayedTreatment()

#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
