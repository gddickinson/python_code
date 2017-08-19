# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 10:12:11 2017

@author: George
"""
import os
import sys
import numpy as np
from PyPDF2 import PdfFileReader
from collections import Counter
from collections import OrderedDict
from matplotlib import pyplot as plt
import glob


def getWordList(filename, minWordLength = 2, maxWordLength = 25):
    

    def parsePDF(filename):
        parseList = []
        wordList = []
        
        f = open(filename, 'rb')
        reader = PdfFileReader(f)
        pages = reader.numPages
        
        for i in range(pages):
            contents = reader.getPage(i).extractText().split(' ')
            for line in contents:
                line = line.encode('ascii', 'ignore').decode('ascii') #strips out international symbols but gets rid of problems with compatibility between unicode and strings
                for word in line.replace('\n', ' ').replace('(', ' ').replace(')', ' ').replace('[', ' ').replace(']',' ').replace('"', ' ').replace('\\', ' ').replace('/', ' ').replace(';', ' ').replace('*', ' ').replace('', ' ').replace('&', ' ').replace('€', ' ').replace('£', ' ').replace('$', ' ').replace(':', ' ').replace('=', ' ').replace('.', ' ').split(','):
                    #word = word.replace(' ','').lower()
                    word = word.replace(' ','')
                    word = word.replace('{', '').replace('}','')
                    word = ''.join([i for i in word if not i.isdigit()])
                    if len(word) < maxWordLength:
                        parseList.append(word)
                                
        f.close()
        
        for word in parseList:
            if len(word)> 1:
                wordList.append(word)

        print('file parsed')
        #print (wordList)
        return wordList
    
    
    ###########################################################
    parselist = parsePDF(filename)

    print(sorted(parselist))
   
    wc = OrderedDict()
    for w in parselist:
        if len(w) >= minWordLength:
            wc[w] = wc.get(w, 0) + 1

    print('ordered list created')
    
    finalList = list(wc.items())    
    finalList = [word for word in finalList if word[1] >= 1] #report if more than 2 occurences detected
    finalList.sort(key=lambda tup: tup[1])
    finalList.reverse()
    
    print(finalList[:100]) #prints top 100 most frequent words detected 
    
    #words = [word[0] for word in finalList][:20]
    #score = [int(word[1]) for word in finalList][:20]
    #x_pos = range(len(words)) 
    
      
    #plt.bar(x_pos, score)
    #plt.xticks(x_pos, words, rotation='vertical', horizontalalignment='center') 
    #plt.ylabel('Word Frequency')
    #plt.show()
    
    return finalList, parselist


path = r'C:\Users\George\Desktop'
file = 'science.aam9321.full' 

filename = path + '\\' + file + '.pdf'

wordList, parselist = getWordList(filename, minWordLength = 2, maxWordLength = 25) 

upperCaseWords = []
for word in parselist:
    if word[0].isupper() and word[1].isupper():
        if word not in upperCaseWords:
            upperCaseWords.append(word)
    

np.savetxt(path + '\\' + file + '_result.txt', wordList, fmt="%s",delimiter=',')
print('file 1 saved as:' + path + '\\' + file + '_result.txt')

np.savetxt(path + '\\' + file + '_upperCase_result.txt', upperCaseWords, fmt="%s",delimiter=',')
print('file 2 saved as:' + path + '\\' + file + '_result.txt')
