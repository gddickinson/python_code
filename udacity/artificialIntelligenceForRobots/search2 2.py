# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 19:37:57 2016

@author: George
"""

# -----------
# User Instructions:
# 
# Modify the function search so that it returns
# a table of values called expand. This table
# will keep track of which step each node was
# expanded.
#
# Make sure that the initial cell in the grid 
# you return has the value 0.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]
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
    # modify code below
    # ----------------------------------------
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    x = init[0]
    y = init[1]
    g = 0
    n = 1
    open = [[g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand
    
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    expand[init[0]][init[1]] = 0
 
    move  = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    move[goal[0]][goal[1]] = '*'

    newMove  = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    newMove[goal[0]][goal[1]] = '*'
    
    
    while not found and not resign:
        if len(open) == 0:
            resign = True
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
            
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            expand[x2][y2] = n
                            move[x][y] = delta_name[i]
                            n += 1
                            closed[x2][y2] = 1

    position = init
    while position[0] != goal[0] or position[1] != goal[1]:
        newMove[position[0]][position[1]] = move[position[0]][position[1]]
        for i in range(len(delta_name)):
            if move[position[0]][position[1]] == delta_name[i]:
                position[0] = position[0]+delta[i][0]
                position[1] = position[1]+delta[i][1]
                newMove[position[0]][position[1]] = move[position[0]][position[1]]

    return newMove

#print (search(grid,init,goal,cost))
test = (search(grid,init,goal,cost))

for i in range(len(test)):
    print(test[i])