# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 19:57:24 2015

@author: george
"""

import numpy as np
import sympy
import random
import matplotlib.pyplot as plt
import math
import time


class World(object):
    """
    Create the array that defines the world and keeps track of time, positions of questions
    and answerFunctions
    Updates new positions after each round
    """

    def __init__(self, width = 1000, height = 1000, questionList =[], answerFunctionList=[]):
        """
        Initiate world array and lists of questions and answerFunctions
        """

        self.cyto = np.zeros((width,height))
        self.width = width
        self.height = height
        self.questionList = questionList
        self.answerFunctionList = answerFunctionList

    def addQuestion (self, questionList):
        self.questionList = self.questionList + questionList
        return

    def addAnswerFunction (self, answerFunctionList):
        self.answerFunctionList = self.answerFunctionList + answerFunctionList
        return

    def getQuestions(self):
        ans = []
        for question in self.questionList:
            ans.append((question.getX(),question.getY()))
        return ans

    def getAnswerFunctions (self):
        ans = []
        for answerFunction in self.answerFunctionList:
            ans.append((answerFunction.getX(),answerFunction.getY()))
        return ans


class QuestionMaker(object):
    """
    Generates random Question and Answer 
    """
    
    def __init__(self, x, y, world):
        self.x = x  
        self.y = y
        self.world = world
        self.question = None
        self.answer = None
        self.questionType = None
        self.answerType = None
        while self.answerType == None:
            try:
                self.generateQuestion()
                self.generateAnswer()
            except:
                pass

    def getQuestion(self):
        return self.question

    def getQuestionType(self):
        return self.questionType

    def getAnswer(self):
        return self.answer

    def getAnswerType(self):
        return self.answerType

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y    

    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
    
    def generateQuestion(self):
        """
        Generate random math problem of type x [operator] y = z
        """
        operatorList = ['/', '*', '+', '-', '%', '**']
        operator = random.choice(operatorList)
        if random.random()>0.5:
            x = str(random.randint(0,9))
        else:
            x = str(random.uniform(0,1000))
        
        if random.random()>0.5:
            y = str(random.randint(0,9))
        else:
            y = str(random.uniform(0,1000))
        
        
        problem = x+' '+operator+' '+y
        operatorDict = {'/': 'division', '*': 'multiplication', '+': 'addition', '-': 'subtraction', '%': 'modulus', '**': 'power'}
        self.questionType = operatorDict[operator]
        self.question = problem
    
    def generateAnswer(self):
        """
        Parse question and return answer
        """
        self.answer = sympy.sympify(self.question)
        answerType = str(type(self.answer)).split('.')[-1]
        answerType = answerType.split("'")[0]
        self.answerType = answerType
        self.answer = str(self.answer)
        
class AnswerFunction(object):
    """
    object that attempts to answer questions it encounters in World
    detects questions and other AnswerFunctions within search radius
    reads question, questionType, answer and answerType
    decide whether to attempt to answer question or to attempt to eat or mate with other AnswerFunction
    uses randomly generated functions to attempt to answer question
    saves randomly generated functions and combinations of functions
    scored on speed of result and nearness of result to correct answer
    score determines likeliness of AnswerFunction surviving to next round
    """

    def __init__(self, x, y, world, score = 100, searchRadius = 10, movementType = 'random', survivalChance = 1.0, reproductionChance = 0.5):
        self.x = x  
        self.y = y
        self.world = world
        self.score = score
        self.searchRadius = searchRadius
        self.movementType = movementType
        #movmentTyoes = random, move Towards or awayfrom questionTypes, move Towards or away from AnswerFunctions
        self.survivalChance = survivalChance
        self.reproductionChance = reproductionChance
        
    def getSurroundingPositions(self, x,y):
        """
        returns valid coordiates in a rectangular world surrounding one x,y position
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

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y    

    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
    

test = World()
question = QuestionMaker(0,0,test)
print (question.getQuestion(), question.getQuestionType(), question.getAnswer(), question.getAnswerType())

       