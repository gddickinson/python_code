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


def getWordList(filename, minWordLength = 2, maxWordLength = 30):
    

    def parsePDF(filename):
        parseList = []
        wordList = []
        
        f = open(filename, 'rb')
        reader = PdfFileReader(f)
        pages = reader.numPages
        
        for i in range(pages):
            contents = reader.getPage(i).extractText().split(' ')
            for line in contents:
                line = line.encode('ascii', 'replace').decode('ascii') #replaces international symbols to get rid of problems with compatibility between unicode and strings

                for word in line.replace('\n', ' ').replace('(', ',').replace(')', ',').replace('{', ',').replace('}',',').replace('[', ',').replace(']',',').replace('"', ',').replace('\\', ',').replace('/', ',').replace('>', ',').replace('<', ',').replace(';', ',').replace('*', ',').replace('&', ',').replace('€', ',').replace('£', ',').replace('$', ',').replace(':', ',').replace('=', ',').replace('?', ',').replace('.', ',').split(','):
                    #word = word.replace(' ','').lower()
                    word = word.replace(' ','')
                    word = ''.join([i for i in word if not i.isdigit()]) #strip out numbers
                    try:
                        if word[0] == '-':
                            word = word.replace('-','')                        
                        
                        if word[-1] == '-':
                            word = word.replace('-','')
                    except:
                        pass
                    #word = ''.join([i for i in word])
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
    parselist1 = parsePDF(filename)
    parselist = []

    #print(sorted(parselist1))

    ###remove blacklisted words ############
    
    dateTime = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'january', 'february', 'april', 'march', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'mon', 'tue', 'wed', 'thr', 'fri', 'jan', 'feb', 'apr', 'may', 'aug', 'sep', 'oct', 'nov', 'dec']
    stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
    blacklist = dateTime + stopwords + ["comment","recommendation","determined","presently","completed","identified","identify","specifically","potentially","currently","information","administration","technical","certainly","later","involved","successfully","portion","concern","bulletin","biology","implemented","editor","preferred","consistent","document","method","concern","authority","detection","encountered","detected","protocol","participant","using","conducted","used","attachment","bird","research","department","lower","rate","result", "resulted","zone","majority","unit","individual","based","species","colorado","arizona","nevada","california","bureau","contacts","contact","program","proportion","included","conservation","wildlife","analysis", "efforts", "model", "modelling", "district", "estimates", "report", "estimate", "data", "location"]
    blacklist2 =[]
  
    for word in blacklist:
        blacklist2.append(word.title())

    blacklist = blacklist + blacklist2

    for word in parselist1:
        if word not in blacklist:
            parselist.append(word)
   
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
    
    words = [word[0] for word in finalList][:20]
    score = [int(word[1]) for word in finalList][:20]
    x_pos = range(len(words)) 
    
      
    plt.bar(x_pos, score)
    plt.xticks(x_pos, words, rotation='vertical', horizontalalignment='center') 
    plt.ylabel('Word Frequency')
    plt.show()
    
    return finalList, parselist


path = r'C:\Users\George\Desktop\NatureConservancy'
file = 'easlon & bloom_2014' 

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
