def uniqueValues(aDict):
    '''
    aDict: a dictionary
    returns: a sorted list of keys that map to unique aDict values, empty list if none
    '''
    testDict = aDict.copy()
    valuesToKeep = []
    value_track= []
    ans = []
    for key in testDict:
        valuesToKeep.append(testDict[key])
    
    for number in range(len(valuesToKeep)):
        value_track.append(0)
        
    for value in range(len(valuesToKeep)):
        for x in range(len(valuesToKeep)):
            if valuesToKeep[value] == valuesToKeep[x]:
                value_track[value] +=1
                
    for x in range(len(value_track)):
        if value_track[x] == 1:
            ans.append(testDict.keys()[testDict.values().index(valuesToKeep[x])])
            
    ans = sorted(ans)
   
    return ans
    
    
#aDict = {1: 1, 3: 2, 6: 0, 7: 0, 8: 4, 10: 0}
aDict = {1: 1, 2: 1, 3: 1}
print (uniqueValues(aDict))