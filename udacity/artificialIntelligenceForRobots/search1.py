# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):
    # ----------------------------------------
    # insert code here
    # ----------------------------------------

    def returnSpaceState(position,grid):
        try:
            if position[0] < 0:
                return False
            if position[1] < 0:
                return False
            if grid[position[0]][position[1]] == 0:
                return True
        except:
            pass 
        return False

    openList = []
    openList.append(init)
    closedList = openList
    g = 0

    def checkList(position, closedList):
        for i in range(len(closedList)):
            if position[0] == closedList[i][0]:
                if position[1] == closedList[i][1]:
                    return True
        return False
    
    def expandList (openList, closedList, grid, g, cost):
        newOpenList=[]
        for i in range(len(openList)):
            for j in range(len(delta)):
                if returnSpaceState([(openList[i][0] + delta[j][0]), (openList[i][1] + delta[j][1])],grid):
                    if len(closedList) == 0:
                        newOpenList.append([openList[i][0]+delta[j][0],openList[i][1]+delta[j][1]])
                    else:
                        if checkList([openList[i][0]+delta[j][0],openList[i][1]+delta[j][1]], closedList) == False:
                            if checkList([openList[i][0]+delta[j][0],openList[i][1]+delta[j][1]], newOpenList) == False:
                                newOpenList.append([openList[i][0]+delta[j][0],openList[i][1]+delta[j][1]])
                            
        for i in range(len(newOpenList)):
            closedList.append(newOpenList[i])

        g += cost
        return newOpenList, closedList, g

    numberOfSpaces = len(grid) * len(grid[0])

    for i in range(numberOfSpaces):  
        openList, closedList, g = expandList(openList,closedList,grid,g,cost)
        if checkList(goal, openList):
            return [g, openList[0][0], openList[0][1]]


    return 'fail'
print (search(grid,init,goal,cost))



