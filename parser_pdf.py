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

def getProjectWordList(projectCode, path, searchWords=[]):
    
    filename2 = path + r'\commonWords.txt'
    files_in_dir = os.listdir(path)
     
    #### get blacklisted words ####
    commonWords = np.loadtxt(filename2,delimiter = ',', dtype = type(str))
    commonWordList = []
    
    for word in commonWords:
        newword = (word.split("'")[1])
        commonWordList.append(newword.split(' ')[0])
    
       
    dateTime = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'january', 'february', 'april', 'march', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'mon', 'tue', 'wed', 'thr', 'fri', 'jan', 'feb', 'apr', 'may', 'aug', 'sep', 'oct', 'nov', 'dec']
    stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
    blacklist1 = ["comment","recommendation","determined","presently","completed","identified","identify","specifically","potentially","currently","information","administration","technical","certainly","later","involved","successfully","portion","concern","bulletin","biology","implemented","editor","preferred","consistent","document","method","concern","authority","detection","encountered","detected","protocol","participant","using","conducted","used","attachment","bird","research","department","lower","rate","result", "resulted","zone","majority","unit","individual","based","species","colorado","arizona","nevada","california","bureau","contacts","contact","program","proportion","included","conservation","wildlife","analysis", "efforts", "model", "district", "estimates", "report", "estimate", "data", "location"]
    blacklist2 = []
    for word in blacklist1:
        blacklist2.append(word+'s')
    
    blackList = stopwords + dateTime + commonWordList + blacklist1 + blacklist2
    whiteList = ['mark', 'recapture', 'photo', 'photograph'] + searchWords
    
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
    i = 0
    for file in files_in_dir:
        if file.split('_')[0] == projectCode:
            try:
                print(file)
                word_list = parsePDF(os.path.join(path,file))

                if i == 0:
                    projectList = word_list
                else:
                    for word in word_list:
                        if word in projectList:
                            projectList.append(word)
    
            except:
                print('finished project')
            i+=1
    
    wc = OrderedDict()
    for w in projectList:
        if len(w) >= 3:
            if searchWords != []:
                for targetWord in searchWords:
                    if w == targetWord:
                        wc[w] = wc.get(w, 0) + 1

            else:
                wc[w] = wc.get(w, 0) + 1
    
    projectFinalList = list(wc.items())
    projectFinalList = [word for word in projectFinalList if word[1] >= 3]
    projectFinalList.sort(key=lambda tup: tup[1])
    projectFinalList.reverse()
    
    #print(projectFinalList[:100])
    
   # words = [word[0] for word in projectFinalList][:20]
    #score = [int(word[1]) for word in projectFinalList][:20]
    #x_pos = range(len(words)) 
    
      
    #plt.bar(x_pos, score)
    #plt.xticks(x_pos, words, rotation='vertical', horizontalalignment='center') 
    #plt.ylabel('Word Frequency')
    #plt.show()
    
    return projectFinalList

def getProjectCodes(path):
    fileList = []
    codeList = []
    #numberFiles = []
    
    #path = r'C:\Users\George\Dropbox\LCR_webpages\mass_download\Reports'
    #output = path + r'\fileList_result.txt'
    #output2 = path + r'\codeList_result.txt'
    path = path + r'\**\*.pdf'
    
    for filename in glob.iglob(path, recursive=True):
        fileList.append(str(os.path.split(filename)[1]))
    
    
    for file in fileList:
        if file.split("_")[0] not in codeList:
            codeList.append(file.split("_")[0])
        
    
    #np.savetxt(output, fileList, delimiter=',', fmt="%s")
    #np.savetxt(output2, codeList, delimiter=',', fmt="%s")
    return codeList


##############################################################################


organismWords = ["avian","fish","bird","amphibian","bat", "frog", "rat", "insect", "mussel", "vegetation", "plant","tree", "shrub", "veligers", "bacteria", "willow", "quailbush", "cedar", "mesquite", "arrowweed", "cottonwood", "cottonwood-willow","razorback", "rasu", "flannelmouth", "yellow-billed", "bonytail","rainbow", "trout","catfish", "bass","cuckoo","owl","elf-owl", "woodpecker", "warbler", "flycatcher", "tanger", "flicker", "vireo", "grackel","quail","blackbird","starling", "dove","adult", "juvenile", "larvae", "larval", "breeder", "migrants", "waterbirds", "shorebirds", "phytoplankton","zooplankton", "plankton", "copepod","cyanobacteria", "bacillariophyta", "chlorophyta", "cryptophyta","pyrrohyta"]
placeWords = ["estury","freshwater","coastal","riparian","lake", "marsh", "channel", "backwater","pond","ditch", "raceway", "soil", "tank","laboratory", "hatchery", "reservoir", "floodplain", "herbaceous", "crop", "woody", "canopy", "understory", "snag", "irrigation", "wildfire", "wetland", "forest", "sediment", "roost","foliage", "sand"]
chemicalWords = ["oxygen", "nitrogen", "carbon", "potassium", "phosphorous", "orthophosphorous", "ammonia","formalin","salinity", "nitrate", "nitrite", "ph","acid","alkaline", "acidity", "alkalinity", "arsenic", "conductivity","biomass", "pozzolan", "lassenite","humidity"]
technicalWords = ["mist-netting","demography","post-stocking","telemetry","shannon-wiener", "diversity","epa", "anova","abiotic","clearing","monitoring","densiometer","point-intercept","survey","singing","display","search","grid-search","creation","restoration","population","acoustic","recruitment","gis","satellite","map","disease","swimming","growth","mass", "height", "weight", "density", "moisture", "temperature","trial", "treatment","tolerance","mortality","netting","transponder","trapping","trap","capture","release","mark", "recapture", "mark-recapture", "electrofishing","sampling", "double-sampling", "transmitters","tagging", "tagged", "track","tracking","transect","sensor", "photo", "photograph", "genetic", "dna", "haplotype","tissue", "cell", "microscope", "microscopy","microscopic", "staining", "planting", "fungus", "survivorship", "stocking", "spawning", "habitat", "nest", "nesting","eggs", "predation","predator", "prey","breeding", "survival", "foraging","fertilization"]

searchWords = organismWords + placeWords + technicalWords

path = r'C:\Users\George\Desktop\report_no_dir'


pCodes = getProjectCodes(path)
#pCodes = ['b1','c8']

finalList = np.array(['project']+searchWords,dtype='str')

#ucomment to get list of all words in a project
#projectCode = 'g4'
#allWords = getProjectWordList(projectCode, path)

for code in pCodes:
    try:
        searchWordNList = []
    
        for word in searchWords:
            searchWordNList.append('0')
    
        pWordList = getProjectWordList(code, path, searchWords)
    
        for i in range(len(searchWords)):
            for word in pWordList:
                if searchWords[i] == word[0] or searchWords[i]+'s' == word[0] or searchWords[i]+'d' == word[0]:
                    searchWordNList[i] = str(word[1])
        
        result = np.array([code]+searchWordNList,dtype='str')

        finalList = np.vstack((finalList, result))
    except:
        print("A miss: " + code)
        pass
    

np.savetxt(path+r'\searchResult'+'.txt',finalList, fmt="%s",delimiter=',')



