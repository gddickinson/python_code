# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 17:29:24 2018

@author: George
"""

import random
import numpy as np
from gridData import Grid
from collections import Counter
from tqdm import tqdm
from copy import deepcopy


MUTATION_RATE = 0.005

CODONLIST = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','Z']


DNA_MAX = 4000
DNA_INIT = 300

def generateDNA():
    return np.random.choice(CODONLIST, DNA_INIT, replace=True)

def concat(l):
    ans = ''
    for letter in l:
        ans += letter
    return ans

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
    
GENE_LENGTH = 3

GENE_00 = 'AA'     #replicate self
GENE_01 = 'BB'     #sexualy reproduce with another with same gene
GENE_02 = 'CC'     #convert nutrient_A -> nutrient_B gain NUTRIENT_A energy/2
GENE_03 = 'DD'     #convert nutrient_B-> nutrient_C gain NUTRIENT_B energy/2
GENE_04 = 'EE'     #convert nutrient_B + nutrient_C -> NUTRIENT_A gain NUTRIENT_C/2
GENE_05 = 'FF'     #move 1 step in direction of usuable nutrient with highest energy
GENE_06 = 'GG'     #skip next gene
GENE_07 = 'HH'     #PREDATOR - consume another on square for all their energy unless they also have more numbers of gene or a defensive gene
GENE_08 = 'II'     #move 1 step away from a PREDATOR
GENE_09 = 'JJ'     #move 1 step toward a PREDATOR
GENE_11 = 'KK'     #DEFENDER - protects from being eaten unless PREDATOR has 5x as many PREDATOR genes
GENE_12 = 'LL'     #move 1 step toward a DEFENDER
GENE_13 = 'MM'     #move 1 step away from a DEFENDER
GENE_14 = 'NN'     #Identify as FAMILY1_X X depends on number of genes
GENE_15 = 'OO'     #Identify as FAMILY2_X X depends on number of genes
GENE_16 = 'PP'     #Identify as FAMILY3_X X depends on number of genes
GENE_17 = 'QQ'     #move toward closest family member
GENE_18 = 'RR'     #move away from closest family member
GENE_19 = 'SS'     #Identify as FAMILY3_X X depends on number of genes
GENE_20 = 'TT'     #steal random gene from another

ALLGENES = [GENE_00, GENE_01, GENE_02, GENE_03, GENE_04, GENE_05, GENE_06,
            GENE_07, GENE_08, GENE_09, GENE_11, GENE_12, GENE_13,
            GENE_14, GENE_15,GENE_16, GENE_17, GENE_18, GENE_19, GENE_20 ]

WORLD_SIZE = 8

RUNLENGTH = 1000

class World():
    def __init__(self, worldSize):
        self.worldSize = worldSize
        #track position of cells
        self.initialiseCellGrid()
        #track nutrients in seperate grids - same index
        self.nutrientA_Grid = np.random.randint(1000, size=(self.worldSize,self.worldSize))
        self.nutrientB_Grid = np.zeros((self.worldSize,self.worldSize),dtype=int)
        self.nutrientC_Grid = np.zeros((self.worldSize,self.worldSize),dtype=int)
        self.dominantGrid = np.zeros((self.worldSize,self.worldSize),dtype="<U10")
        self.totalCellNumber = 0
        self.cellList = []
                
    def initialiseCellGrid(self):
        self.cellGrid = np.empty((self.worldSize,self.worldSize),dtype=object)
        for (x,y), value in np.ndenumerate(self.cellGrid):
            self.cellGrid[x,y] = []
        
    def printGrid(self):
        print(self.cellGrid)
        
    def getGridDominant(self):
        newTotalCells = 0
        self.cellList = []
        for (x,y), value in np.ndenumerate(self.cellGrid):
            self.dominantGrid[x,y] = self.getDominantforList(x,y)
            if self.dominantGrid[x,y] != 'None':
                newTotalCells = newTotalCells + len(self.cellGrid[x,y])
                self.cellList.extend(self.cellGrid[x,y]) 
        self.totalCellNumber = newTotalCells
        return self.dominantGrid
        
    def addCell(self, cellList):
        for cell in cellList:
            self.cellGrid[cell.getPosition()].append(cell)

    def getCellCount(self):
        return self.totalCellNumber
        
    def getGridContentList(self, x, y):
        ans = []
        for row in self.cellGrid[x,y]:
            ans.append(row.getName())
        return(ans)

    def updateGridCellPositions(self):
        for (x,y), value in np.ndenumerate(self.cellGrid):
            for i in range(len(self.cellGrid[x,y])):
                try:
                    cell = self.cellGrid[x,y][i]
                    testX, testY = cell.getPosition()
                    if testX != x or testY != y:
                        self.cellGrid[x,y].pop(i)
                        self.addCell([cell])
                except:
                    pass


    def getDominantforList(self, x, y):
        try:
            names = self.getGridContentList(x,y)
            name, value = Counter(names).most_common(1)[0]
            return name
        except:
            return 'None'

    def getNutrients(self, x, y):
        return [self.nutrientA_Grid[x,y], self.nutrientB_Grid[x,y], self.nutrientC_Grid[x,y]]

    def updateNutrients(self, x, y, A, B, C):
        self.nutrientA_Grid[x,y] = self.nutrientA_Grid[x,y] + A
        self.nutrientB_Grid[x,y] = self.nutrientB_Grid[x,y] + B
        self.nutrientC_Grid[x,y] = self.nutrientC_Grid[x,y] + C

    def getNumberOfCellsEachCell(self):
        self.cellNumberGrid = np.zeros((self.worldSize,self.worldSize),dtype=int)
        for (x,y), value in np.ndenumerate(self.cellGrid):
            self.cellNumberGrid[x][y] = len(self.cellGrid[x][y])
        return self.cellNumberGrid
        
    def getAllGenes(self):
        #TODO
        self.allGenesInWorld = []
        for cell in self.cellList:
            self.allGenesInWorld.append(cell.getGenes())
        return Counter(self.allGenesInWorld)

    def getHigherNutrients(self, x, y, nutrient):
        if nutrient == 'A':
            testGrid = self.nutrientA_Grid
        if nutrient == 'B':
            testGrid = self.nutrientB_Grid
        if nutrient == 'C':
            testGrid = self.nutrientC_Grid

        newX = x
        newY = y
        
        currentValue = testGrid[x,y]
         
        try:
            UPvalue = testGrid[x,y+1]
        except:
            UPvalue = 0
        try:
            DOWNvalue = testGrid[x,y-1]
        except:
            DOWNvalue = 0
        try:
            LEFTvalue = testGrid[x-1,y]
        except:
            LEFTvalue = 0
        try:
            RIGHTvalue = testGrid[x+1,y]
        except:
            RIGHTvalue = 0

        if currentValue < UPvalue:
            currentValue = UPvalue
            newX = x
            newY = y+1
        
        if currentValue < DOWNvalue:
            currentValue = DOWNvalue
            newX = x
            newY = y-1

        if currentValue < LEFTvalue:
            currentValue = LEFTvalue
            newX = x-1
            newY = y

        if currentValue < RIGHTvalue:
            currentValue = RIGHTvalue
            newX = x+1
            newY = y

        return newX,newY

    def updateCellGrid(self):
        for (x,y), value in np.ndenumerate(self.cellGrid):
            for cell in self.cellGrid[x,y]:
                if cell.getStatus() == False:
                    self.cellGrid[x,y].pop(cell)
            

    def updateCells(self):
        for cell in self.cellList:
            if cell.getStatus():
                cell.update()

    def update(self):
        self.updateGridCellPositions()
        self.getGridDominant()
        self.updateCells()
        print(self.getCellCount())
        
        

class Cell():
    def __init__(self, x,y, energy, DNA, name, world):
        self.x = x
        self.y = y
        self.energy = energy
        self.DNA = DNA
        self.updateGeneList()
        self.name = name
        self.world = world
        self.chanceToReplicate = 0.1
        self.replicationCost = 10
        self.energyPassedOn = self.replicationCost / 2
        self.alive = True
                
    def getPosition(self):
        return self.x, self.y
    
    def printDNA(self):
        print(self.DNA)
        
    def updateGeneList(self):
        self.geneList = []
        tempGeneList = chunks(self.DNA, GENE_LENGTH)
        for gene in tempGeneList:
            concatinatedGene = concat(gene)
            if self.searchALLGENES(concatinatedGene):  
                self.geneList.append(concatinatedGene)
                
        self.geneCount = Counter(self.geneList)
    
    def printGenes(self):
        print(self.geneCount) 
    
    def searchALLGENES(self, gene):
        for searchGene in ALLGENES:
            if searchGene in gene:
                return True
    
    def getName(self):
        return self.name
    
    def getGenes(self):
        return self.geneList
        
    def geneTest(self, geneType):
        for gene in self.geneList:
            if geneType in gene:
                return True

    def getStatus(self):
        return self.alive

    def death(self):
        self.alive = False

    def mutate(self, DNA):
        newDNA = deepcopy(DNA)
        for i in range(len(newDNA)):
            if random.random() < MUTATION_RATE:
                newDNA[i] = random.choice(CODONLIST)
        return newDNA
        

    def replicate(self):
        if random.random() < self.chanceToReplicate:
            world.addCell([Cell(self.x, self.y, self.energyPassedOn, self.mutate(self.DNA), self.name, self.world)])
            self.energy = self.energy - self.replicationCost
            
    def eat_A(self):
        if self.world.getNutrients(self.x, self.y)[0] > 0:
            self.energy = self.energy + 1
            world.updateNutrients (self.x, self.y, -1, 1, 0)
            
    def moveToEat_A(self):
        self.x, self.y = world.getHigherNutrients(self.x,self.y,'A')

    def eat_B(self):
        if self.world.getNutrients(self.x, self.y)[1] > 0:
            self.energy = self.energy + 1
            world.updateNutrients (self.x, self.y, 0, -1, 1)
            
    def moveToEat_B(self):
        self.x, self.y = world.getHigherNutrients(self.x,self.y,'B')
                   
    def update(self):
        self.energy = self.energy - 1
        
        if self.energy < 1:
            self.death()
            return       

        if self.geneTest(GENE_00):
            self.replicate()
        
        if self.geneTest(GENE_02):
            self.eat_A()
            if self.geneTest(GENE_05):
                self.moveToEat_A()
        
        #TODO cells don't appear to move if this actvated
        #if self.geneTest(GENE_03):
        #    self.eat_B()
        #    if self.geneTest(GENE_05):
        #        self.moveToEat_B()


##############################################################################
        
world =  World(WORLD_SIZE) 

testDNA1 = np.array(['A', 'A', 'S', 'C', 'C', 'F', 'F', 'F', 'N', 'T', 'Q', 'A', 'I',
       'G', 'H', 'K', 'H', 'P', 'F', 'M', 'M', 'I', 'O', 'H', 'N', 'T',
       'J', 'C', 'H', 'Q', 'P', 'O', 'O', 'S', 'D', 'D', 'J', 'T', 'I',
       'Z', 'C', 'L', 'Z', 'Q', 'A', 'Q', 'Q', 'L', 'P', 'Q', 'B', 'J',
       'T', 'I', 'K', 'A', 'F', 'D', 'O', 'O', 'B', 'D', 'N', 'T', 'P',
       'D', 'J', 'K', 'D', 'G', 'L', 'S', 'Q', 'B', 'A', 'E', 'O', 'F',
       'F', 'N', 'S', 'Z', 'R', 'L', 'F', 'A', 'P', 'J', 'E', 'A', 'A',
       'O', 'K', 'Z', 'C', 'H', 'H', 'A', 'E', 'Q', 'E', 'M', 'F', 'H',
       'J', 'T', 'Z', 'D', 'T', 'A', 'H', 'T', 'Z', 'G', 'E', 'Z', 'L',
       'I', 'L', 'E', 'R', 'P', 'K', 'L', 'I', 'K', 'N', 'S', 'L', 'H',
       'Z', 'Z', 'J', 'H', 'O', 'R', 'C', 'Q', 'O', 'R', 'R', 'G', 'P',
       'K', 'B', 'J', 'E', 'J', 'C', 'Q', 'M', 'C', 'F', 'M', 'P', 'C',
       'Z', 'F', 'S', 'E', 'G', 'E', 'L', 'C', 'H', 'S', 'R', 'R', 'I',
       'O', 'I', 'T', 'I', 'A', 'S', 'T', 'D', 'K', 'Q', 'M', 'A', 'B',
       'J', 'P', 'T', 'H', 'T', 'R', 'E', 'N', 'A', 'K', 'N', 'B', 'M',
       'T', 'K', 'J', 'S', 'Q', 'F', 'A', 'J', 'H', 'G', 'S', 'B', 'I',
       'C', 'E', 'E', 'M', 'I', 'S', 'C', 'K', 'N', 'P', 'K', 'O', 'I',
       'M', 'G', 'M', 'T', 'R', 'A', 'L', 'G', 'H', 'K', 'E', 'L', 'S',
       'E', 'D', 'M', 'T', 'L', 'D', 'M', 'G', 'T', 'M', 'S', 'A', 'N',
       'G', 'J', 'N', 'A', 'Q', 'D', 'C', 'P', 'D', 'C', 'R', 'R', 'E',
       'S', 'L', 'A', 'P', 'H', 'R', 'Q', 'N', 'S', 'Q', 'S', 'D', 'R',
       'B', 'J', 'M', 'R', 'E', 'P', 'N', 'M', 'B', 'Q', 'B', 'B', 'B',
       'L', 'E', 'G', 'L', 'H', 'M', 'N', 'D', 'M', 'M', 'B', 'S', 'Z',
       'J'], dtype='<U1')

testDNA2 = np.array(['A', 'A', 'S', 'C', 'C', 'D', 'F', 'F', 'N', 'T', 'Q', 'A', 'I',
       'G', 'H', 'K', 'H', 'P', 'F', 'M', 'M', 'I', 'O', 'H', 'N', 'T',
       'J', 'C', 'H', 'Q', 'P', 'O', 'O', 'S', 'D', 'D', 'J', 'T', 'I',
       'Z', 'C', 'L', 'Z', 'Q', 'A', 'Q', 'Q', 'L', 'P', 'Q', 'B', 'J',
       'T', 'I', 'K', 'A', 'F', 'D', 'O', 'O', 'B', 'D', 'N', 'T', 'P',
       'D', 'J', 'K', 'D', 'G', 'L', 'S', 'Q', 'B', 'A', 'E', 'O', 'F',
       'F', 'N', 'S', 'Z', 'R', 'L', 'F', 'A', 'P', 'J', 'E', 'A', 'A',
       'O', 'K', 'Z', 'C', 'H', 'H', 'A', 'E', 'Q', 'E', 'M', 'F', 'H',
       'J', 'T', 'Z', 'D', 'T', 'A', 'H', 'T', 'Z', 'G', 'E', 'Z', 'L',
       'I', 'L', 'E', 'R', 'P', 'K', 'L', 'I', 'K', 'N', 'S', 'L', 'H',
       'Z', 'Z', 'J', 'H', 'O', 'R', 'C', 'Q', 'O', 'R', 'R', 'G', 'P',
       'K', 'B', 'J', 'E', 'J', 'C', 'Q', 'M', 'C', 'F', 'M', 'P', 'C',
       'Z', 'F', 'S', 'E', 'G', 'E', 'L', 'C', 'H', 'S', 'R', 'R', 'I',
       'O', 'I', 'T', 'I', 'A', 'S', 'T', 'D', 'K', 'Q', 'M', 'A', 'B',
       'J', 'P', 'T', 'H', 'T', 'R', 'E', 'N', 'A', 'K', 'N', 'B', 'M',
       'T', 'K', 'J', 'S', 'Q', 'F', 'A', 'J', 'H', 'G', 'S', 'B', 'I',
       'C', 'E', 'E', 'M', 'I', 'S', 'C', 'K', 'N', 'P', 'K', 'O', 'I',
       'M', 'G', 'M', 'T', 'R', 'A', 'L', 'G', 'H', 'K', 'E', 'L', 'S',
       'E', 'D', 'M', 'T', 'L', 'D', 'M', 'G', 'T', 'M', 'S', 'A', 'N',
       'G', 'J', 'N', 'A', 'Q', 'D', 'C', 'P', 'D', 'C', 'R', 'R', 'E',
       'S', 'L', 'A', 'P', 'H', 'R', 'Q', 'N', 'S', 'Q', 'S', 'D', 'R',
       'B', 'J', 'M', 'R', 'E', 'P', 'N', 'M', 'B', 'Q', 'B', 'B', 'B',
       'L', 'E', 'G', 'L', 'H', 'M', 'N', 'D', 'M', 'M', 'B', 'S', 'Z',
       'J'], dtype='<U1')
    
cell1 = Cell(0, 0, 100, testDNA1, 'red', world)
cell2 = Cell(7, 7, 100, testDNA2, 'green', world)
world.addCell([cell1, cell2])


for i in tqdm(range(RUNLENGTH)):
    world.update()
     

