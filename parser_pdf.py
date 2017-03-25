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

path = r'C:\Users\George\Desktop\report_no_dir'
filename = path + r'\abiotic_factors_insect_pop_07.pdf'
filename2 = path + r'\commonWords.txt'

projectCode = 'c33'
files_in_dir = os.listdir(path)


#### get blacklisted words ####
commonWords = np.loadtxt(filename2,delimiter = ',', dtype = type(str))
commonWordList = []

for word in commonWords:
    newword = (word.split("'")[1])
    commonWordList.append(newword.split(' ')[0])

dateTime = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'january', 'february', 'april', 'march', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'mon', 'tue', 'wed', 'thr', 'fri', 'jan', 'feb', 'apr', 'may', 'aug', 'sep', 'oct', 'nov', 'dec']
stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
blacklist1 = ["result", "resulted","zone","majority","unit","individual","based","species","colorado","arizona","nevada","california","bureau","contacts","contact","program","proportion","included","conservation","wildlife","analysis", "efforts", "model", "district", "estimates", "report", "estimate", "data", "location"]
blacklist2 = []
for word in blacklist1:
    blacklist2.append(word+'s')

blackList = stopwords + dateTime + commonWordList + blacklist1 + blacklist2
whiteList = ['mark', 'recpture', 'photo', 'photograph']

whiteList2 = []
for word in whiteList:
    whiteList2.append(word+'s')

whiteList = whiteList + whiteList2

def parsePDF(filename):
    parseList = []
    wordList = []
    
    f = open(filename, 'rb')
    reader = PdfFileReader(f)
    pages = reader.numPages
    
    for i in range(pages):
        contents = reader.getPage(i).extractText().split(' ')
        for line in contents:
            for word in line.replace('\n', '').replace('(', '').replace(')', '').replace('[', '').replace(']','').replace('.', '').split(','):
                word = word.replace(' ','').lower()
                word = word.replace('{', '').replace('}','')
                word = ''.join([i for i in word if not i.isdigit()])
                if len(word) < 20:
                    parseList.append(word)
                            
    f.close()
    
    for word in parseList:
        if word in whiteList:
            wordList.append(word)
        elif word not in blackList and len(word)>2:
            wordList.append(word)
    
    
    return wordList


###########################################################
projectList = []

for file in files_in_dir:
    if file.split('_')[0] == projectCode:
        try:
            print(file)
            word_list = parsePDF(os.path.join(path,file))
            projectList = projectList + word_list
        except:
            print('finished project')

wc = OrderedDict()
for w in projectList:
    if len(w) >= 4:
        wc[w] = wc.get(w, 0) + 1

projectFinalList = list(wc.items())
projectFinalList.sort(key=lambda tup: tup[1])
projectFinalList.reverse()
print(projectFinalList[:50])