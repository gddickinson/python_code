# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 08:49:43 2016

@author: george
"""

import numpy as np
import random
import pylab


def makeNormal(mean, sd, numSamples):
    samples = []
    for i in range(numSamples):
        samples.append(random.gauss(mean, sd))
    pylab.hist(samples, bins = 10)
    return samples


#makeNormal(1,0.3,1000)
#makeNormal(10, 0.3, 1000)

class Employee(object):
    """
    Representation of a simple employee
    """
    def __init__(self, job, employeeID):
        """
        Initialize a Employee instance, saves all parameters as attributes
        of the instance.        
        job: greeter or desk
        status: busy or free
        """

        self.job = job
        self.employeeID = employeeID
        self.status = 'free'
        self.busyTime = 0
        self.customersDealtWith = []
        self.currentCustomer = None
        self.timeLeftCurrentJob = 0

    def getJob(self):
        """
        Returns job
        """
        return self.job

    def getEmployeeID(self):
        """
        Returns ID
        """
        return self.employeeID

    def getStatus(self):
        """
        Returns the satus
        """
        return self.status

    def getCustomersDealtWith(self):
        """
        Returns customer list
        """
        return self.customersDealtWith


    def updateStatus (self, entryLine, ticketLine, finished, time):
        """
        If status = free: take available customer based on job type
        if status = busy update times etc
        """
                
        if self.status == 'free':
            if self.job == 'greeter':
                if entryLine != []:
                    self.currentCustomer = entryLine.pop(0)
                    self.currentCustomer.setStatus('beingAllocated')
                    self.currentCustomer.setAllocationTimeStart(time)
                    self.status = 'busy'
                    self.timeLeftCurrentJob = self.currentCustomer.getAllocationTime()
                    return entryLine, ticketLine, finished
                else:
                    return entryLine, ticketLine, finished
            
            elif self.job == 'desk':
                if ticketLine != []:
                    self.currentCustomer = ticketLine.pop(0)
                    self.currentCustomer.setStatus('beingServed')
                    self.currentCustomer.setProblemTimeStart(time)
                    self.status = 'busy'
                    self.timeLeftCurrentJob = self.currentCustomer.getProblemTime()
                    return entryLine, ticketLine, finished
                else:
                    return entryLine, ticketLine, finished              
                
        elif self.status == 'busy':        
            if self.job == 'greeter': 
                if (time - self.currentCustomer.getAllocationTimeStart()) >= self.currentCustomer.getAllocationTime():
                    if random.random() > 0.1:
                        self.currentCustomer.setStatus('waitingService')
                        ticketLine.append(self.currentCustomer)
                        self.currentCustomer.setAllocationTimeEnd(time)
                        self.status = 'free'
                        self.customersDealtWith.append(self.currentCustomer)
                        self.currentCustomer = None
                        #print('allocated')
                        return entryLine, ticketLine, finished
                    else:
                        self.currentCustomer.setStatus('finished')
                        finished.append(self.currentCustomer)
                        self.customersDealtWith.append(self.currentCustomer)
                        self.currentCustomer.setProblemTimeEnd(time)
                        self.status = 'free'
                        self.currentCustomer = None 
                        return entryLine, ticketLine, finished
                    
                else:
                    return entryLine, ticketLine, finished
            
            elif self.job == 'desk': 
                if (time - self.currentCustomer.getProblemTimeStart()) >= self.currentCustomer.getProblemTime():
                    self.currentCustomer.setStatus('finished')                    
                    self.currentCustomer.setProblemTimeEnd(time)
                    self.status = 'free'
                    self.customersDealtWith.append(self.currentCustomer)
                    finished.append(self.currentCustomer)
                    #print('finished')
                    self.currentCustomer = None
                    return entryLine, ticketLine, finished
                else:
                    return entryLine, ticketLine, finished            

        return
    

class EmployeePrioritizer(Employee):
    
    def updateStatus (self, entryLine, ticketLine, finished, time):
        """
        If status = free: take available customer based on job type
        if status = busy update times etc
        """
                
        if self.status == 'free':
            if self.job == 'greeter':
                if entryLine != []:
                    self.currentCustomer = entryLine.pop(0)
                    self.currentCustomer.setStatus('beingAllocated')
                    self.currentCustomer.setAllocationTimeStart(time)
                    self.status = 'busy'
                    self.timeLeftCurrentJob = self.currentCustomer.getAllocationTime()
                    return entryLine, ticketLine, finished
                else:
                    return entryLine, ticketLine, finished
            
            elif self.job == 'desk':
                if ticketLine != []:
                    self.currentCustomer = ticketLine.pop(0)
                    self.currentCustomer.setStatus('beingServed')
                    self.currentCustomer.setProblemTimeStart(time)
                    self.status = 'busy'
                    self.timeLeftCurrentJob = self.currentCustomer.getProblemTime()
                    return entryLine, ticketLine, finished
                else:
                    return entryLine, ticketLine, finished              
                
        elif self.status == 'busy':        
            if self.job == 'greeter': 
                if (time - self.currentCustomer.getAllocationTimeStart()) >= self.currentCustomer.getAllocationTime():
                    if random.random() > 0.1:
                        self.currentCustomer.setStatus('waitingService')
                        if self.currentCustomer.getProblemTime() > 100:
                            print(self.currentCustomer.getProblemTime())
                            ticketLine.insert(0,self.currentCustomer)
                        else:
                            ticketLine.append(self.currentCustomer)
                        self.currentCustomer.setAllocationTimeEnd(time)
                        self.status = 'free'
                        self.customersDealtWith.append(self.currentCustomer)
                        self.currentCustomer = None
                        #print('allocated')
                        return entryLine, ticketLine, finished
                    else:
                        self.currentCustomer.setStatus('finished')
                        finished.append(self.currentCustomer)
                        self.customersDealtWith.append(self.currentCustomer)
                        self.currentCustomer.setProblemTimeEnd(time)
                        self.status = 'free'
                        self.currentCustomer = None 
                        return entryLine, ticketLine, finished
                    
                else:
                    return entryLine, ticketLine, finished
            
            elif self.job == 'desk': 
                if (time - self.currentCustomer.getProblemTimeStart()) >= self.currentCustomer.getProblemTime():
                    self.currentCustomer.setStatus('finished')                    
                    self.currentCustomer.setProblemTimeEnd(time)
                    self.status = 'free'
                    self.customersDealtWith.append(self.currentCustomer)
                    finished.append(self.currentCustomer)
                    #print('finished')
                    self.currentCustomer = None
                    return entryLine, ticketLine, finished
                else:
                    return entryLine, ticketLine, finished


class Customer (object):
    """
    Representation of a simple customer
    """
    def __init__(self, allocationTime, problemTime, customerID):
        """
        Initialize a Employee instance, saves all parameters as attributes
        of the instance.  
        allocationTime: time to allocate to ticketLine (float)
        problemTime: time needed to solve problem (float)
        status: waitingAllocation, beingAllocated, waitingService, beingServed, finished
        """

        self.allocationTime = allocationTime
        if self.allocationTime <1:
            self.allocationTime = 1
        self.problemTime = problemTime
        if self.problemTime <1:
            self.problemTime = 1
        self.cutomerID = customerID
        self.status = 'waitingAllocation'      
        self.waitTime = 0
        self.allocationTimeStart = None
        self.allocationTimeEnd = None
        self.problemTimeStart = None
        self.problemTimeEnd = None
        self.servedTime = 0
        self.startTime = 0

    def getAllocationTime(self):
        """
        Returns allocationTime
        """
        return self.allocationTime

    def getProblemTime(self):
        """
        Returns problemTime
        """
        return self.problemTime

    def getStatus(self):
        """
        Returns the satus
        """        
        return self.status
        
    def setStatus(self, newStatus):
        self.status = newStatus

    def setAllocationTimeStart(self, time):
        self.allocationTimeStart = time

    def setAllocationTimeEnd(self, time):
        self.allocationTimeEnd = time

    def setProblemTimeStart(self, time):
        self.problemTimeStart = time

    def setProblemTimeEnd(self, time):
        self.problemTimeEnd = time

    def getAllocationTimeStart(self):
        return self.allocationTimeStart

    def getProblemTimeStart(self):
        return self.problemTimeStart

    def getProblemTimeEnd(self):
        return self.problemTimeEnd

    def getWaitTime(self):
        """
        Returns the waitTime
        """        
        return self.waitTime

    def getServedTime(self):
        """
        Returns the servedTime
        """        
        return self.problemTimeEnd - self.allocationTimeStart

    def getTotalTime(self):
        """
        Returns the total time waiting
        """        
        return self.problemTimeEnd - self.startTime

def populateCustomerLine(number = 500):
    line = []
    allocationTime = 10 # = 1 minute
    problemLength = 100 # = 10 minutes
    standardDeviation = 20
    for n in range(number):
        line.append(Customer(random.gauss(allocationTime, standardDeviation), random.gauss(problemLength, standardDeviation), n))
    return line


def populateEmployees(desk = 9, greeter = 2):
    staff = []

    for g in range(greeter):
        staff.append(Employee('greeter', desk+g))
        #staff.append(EmployeePrioritizer('greeter', desk+g))
    for d in range(desk):
        staff.append(Employee('desk', d))
        #staff.append(EmployeePrioritizer('desk', d))
    return staff
    
def runSimulationUpdate (entryLine, employees,ticketLine,finished, time):
        """
        
        """

        for each in employees:
            entryLine, ticketLine, finished = each.updateStatus(entryLine, ticketLine, finished, time)

        print(time)        
        return finished

def simulation (numberOfCustomers = 800, numberOfRuns = 50, desk =9, greeter = 2):
    servedTimeMean = []
    totalTimeMean = []
    problemTimeMean = [] 
    customersDealtWithMean = []

    for i in range(numberOfRuns):
        entryLine = populateCustomerLine(numberOfCustomers)
        employees = populateEmployees(desk =9, greeter = 2)
        ticketLine = []
        finished = []
        minutesInDay = (9*60)*10 #timesteps = 1/10 of a minute
            
        for j in range(minutesInDay): 
            finished = runSimulationUpdate(entryLine, employees, ticketLine, finished, time =j)
        
        servedTime = []
        totalTime = []
        problemTime = [] 
        customersDealtWith = []
                
        for each in finished:
            servedTime.append(each.getServedTime())
            totalTime.append(each.getTotalTime())
            problemTime.append(each.getProblemTime())
        
        for each in employees:
            customersDealtWith.append(len(each.getCustomersDealtWith()))
        
        servedTimeMean.append(np.mean(servedTime))
        totalTimeMean.append(np.mean(totalTime))
        problemTimeMean.append(np.mean(problemTime))
        customersDealtWithMean.append(np.mean(customersDealtWith))
            
        #employeeX = range(len(customersDealtWith))
        #pylab.plt.subplot(2, 2, 1)
        #pylab.plot(totalTime)
        #pylab.plot(servedTime)
        #pylab.plot(problemTime)
        #pylab.xlabel('Customer')
        #pylab.ylabel('time (min*10)')
        #pylab.title('Time/customer')
        ##pylab.plt.legend()
        #
        #pylab.plt.subplot(2, 2, 3)
        #pylab.hist(totalTime)
        #pylab.xlabel('time (min*10)')
        #pylab.ylabel('# of customers')
        ##pylab.title('Histogram')
        #
        #pylab.plt.subplot(2, 2, 2)
        #pylab.bar(employeeX,customersDealtWith)
        #pylab.xlabel('employee')
        #pylab.ylabel('# of customers dealt with')
        #
        #pylab.plt.subplot(2, 2, 4)
        #pylab.bar(0,numberOfCustomers)
        #pylab.bar(1,len(finished))
        #pylab.xlabel('')
        #pylab.ylabel('# of customers')
        #
        #print("% of customers served = ", ((len(finished)/numberOfCustomers)*100))
        #print('# of customers / employee = ', customersDealtWith)
        #print('mean time customer waiting = ', round(np.mean(totalTime),2))

    return np.mean(servedTimeMean), np.mean(totalTimeMean), np.mean(problemTimeMean), np.mean(customersDealtWithMean)

servedTimeMean = []
totalTimeMean = []
problemTimeMean = [] 
customersDealtWithMean = []

numberStaff = 20

for i in range(numberStaff):
        
    served,total,problem,dealt = simulation(numberOfCustomers = 20, numberOfRuns = 5, desk =i+1, greeter = numberStaff-i+1)
    servedTimeMean.append(served)
    totalTimeMean.append(total)
    problemTimeMean.append(problem) 
    customersDealtWithMean.append(dealt)

pylab.plot(totalTimeMean)
pylab.plot(servedTimeMean)
pylab.plot(problemTimeMean)
pylab.xlabel('# at desks')
pylab.ylabel('time (min*10)')
pylab.plot.legend()
