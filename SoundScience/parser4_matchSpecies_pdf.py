#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:04:46 2017

@author: george
"""

import os
import sys
import numpy as np
from PyPDF2 import PdfFileReader
from collections import Counter
from collections import OrderedDict
from matplotlib import pyplot as plt
import glob
from collections import Counter
from shutil import copy2

#test file
#filename = r"/Users/george/Dropbox/SoundScience/LCR_webpages/CRAB-CRTR_powerpoints/CRTR/results/01_crtr12_five_years_mscp_olson.pdf"

#path = r"/Users/george/Dropbox/SoundScience/LCR_webpages/CRAB-CRTR_powerpoints/CRTR"
path = r"C:\Users\George\Desktop\LCR_Powerpoints"
#test path
#path = r"/Users/george/Desktop/testing"
files_in_dir = os.listdir(path)

#old search terms
extraSearchTerms = ["reptilian","rana","bufo","astragalus","eriogonum","gopherus","phrynosoma","skipper","flat-tailed","hispid","bittern","lizard","toad","reptile","tortoise","woodpecker","parasite","butterfly","rodent","mouse","seed","small-mamal","amphibian","bat", "frog", "rat",  "mussel", "veligers","pikeminnow", "sootywing","bacteria", "tanager","warbler","cow-bird","willow", "quailbush", "cedar", "mesquite", "arrowweed", "cottonwood", "cottonwood-willow","razorback", "rasu", "flannelmouth", "yellow-billed","humpback","chub", "bonytail","rainbow", "trout","catfish", "bass","cuckoo","owl","elf-owl", "woodpecker", "warbler", "flycatcher", "tanger", "flicker", "vireo", "grackel","quail","blackbird","starling", "dove", "juvenile", "larvae", "larval", "breeder", "migrants", "waterbirds", "shorebirds", "phytoplankton","zooplankton", "plankton", "copepod","rotifer","cladoceran","cyanobacteria", "bacillariophyta", "chlorophyta", "cryptophyta","pyrrohyta", "milkvetch", "buckwheat","rail", "clapper", "chairmaker", "bulrush", "cattail", "phragmites", "threesquare","Choeronycteris mexicana", "leptonycteris","myotis", "parastrellus", "eptesicus", "lasiuru","euderma","idionycteris","antrozous","tadarida","nyctinomops","eumops","xyrauchen", "leaf-nose", "empidonax", "coccyzuz", "saltcedar", "saltgrass","desertbloom","tamarisk", "catostomus", "gila","laterallus","rallus", "ixobrychus", "colaptes", "sigmodon"]

######speciesNames###################
birds = ["woodpecker","warbler","tanager","cuckoo", "owl","flycatcher",	"flicker", "vireo", "quail", "blackbird",	"starling", "dove", "migrants",	"waterbirds",	"shorebirds", "yellow.billed"]
fish = ["pikeminnow","razorback", "rasu", "flannelmouth", "humpback",	"chub",	"bonytail", "rainbow",	"trout",	"catfish", "bass"]
plants = ["deciduous", "willow","quailbush",	"cedar",	"mesquite", "arrowweed", "cottonwood", "cottonwood-willow", "milkvetch",	"buckwheat", "saltcedar",	"saltgrass",	"tamarisk"]
insects = ["butterfly",  "sootywing"]
bats = ["bat"]
amphibians = ["amphibian", "frog"]
             
data_combined = birds + fish + plants + insects + bats + amphibians
#########################################
            
####### habitatNames #################
river = ["reach", "river", "tributary", "tributaries", "spring", "freshwater", "riparian", "channel"]
laboratory = ["impoundment", "raceway", "tank", "laboratory", "hatchery"]
lake = ["shore", "lake"]
reservoir = ["reservoir", "sediment", "dam", "pond"]
marsh = ["flood", "floodplain", "wetland","backwater"]
woodland = ["herbaceous",	"woody",	"woodlands", "canopy",	"understory",	"wildfire", "forest", "foliage"]
agricultural = ["agricultural",	"soil", "crop", "irrigation", "ditch", "reclamation", "sediment", "drainage"]
mines = ["mine"]
roosts = ["roost", "roosting"]
# 
# data_combined = river + laboratory + reservoir + lake + marsh + woodland + agricultural + mines + roosts
######################################

####### dataNames ####################

fishTracking = ["submersible","sherman","fyke","electrofishing","sur","hydrophone","pit","trammel","implantation","boat"]
birdTracking  = ["call-playback","banded","banding","mist-netting","vocalization","singing","band"]
birdPlumage  = ["display","plumage","colorimeter"]
trapping  = ["hoop","trapping","trap","capture","captured","release","mark","recapture","mark.recapture","netting","netted"]
tracking  = ["tag","telemetry","track","tracking","passive","active","transponder","transmitters","tagging","tagged","acoustic","sonic"]
physiology  = ["physiology","physiological","growth","mass","height","weight","weighed","disease","aging", "sexed","tissue","cell","microscope","mortality"]
fishPhysiology = ["pectoral","fin","swim","swimming"]
waterChemistry  = ["depth","oxygen","nitrogen","carbon","potassium","phosphorous","ammonia","salinity","nitrate","nitrite","acid","alkalinity","arsenic","selenium","conductivity","turbidity"]
soilChemistry  = ["pozzolan","lassenite","humidity","limnological","hydrology","hydrological"]
gis  = ["gis","satellite","map","mapping"]
hatchery  = ["hatchery.reared","post-stocking","translocation","broodstock","repatriation","stocking","spawning"]
populationStats  = ["distribution","demography","absence","presence","population","diversity","anova","sampling","double-sampling","transect","survivorship","colonization","survival","recruitment"]
genetic  = ["genetic","dna","mtdna","microsatellites","haplotype","dimorphism","taxonomic"]
restoration  = ["evaluation","study","conservation","development","plan","outreach","restoration","planting","clearing","monitoring"]
photography  = ["video", "photo","photograph","photography","orthophotography","imaging"]
predation  = ["predation","predator","prey", "foraging"]
breeding  = ["nest","nesting","eggs","breeding","propagation"]
transport = ["transport","handling","management"]
diet  = ["diet"]
biologicalMeasures = ["biomass","density","moisture","temperature","toxicity","abiotic","habitat"]
survey  = ["survey","search","sampled","aerial","visual","helicopter"]
fertilizer  = ["fertilization","fertilizer"]


#dict of listed species and their potential search words
listedSpecies = {
"Relict_Leopard_Frog":["Lithobates", "onca", "Rana", "Relict", "Leopard", "Frog"],\
"Colorado_River_Toad":["Bufo","Incilius", "alvarius", "Toad"],\
"Lowland_Leopard_Frog":["Lithobates", "Rana", "yavapaiensis","Lowland","Leopard","Frog"],\
"Arizona_Bell's_Vireo":["Vireo", "bellii", "arizonae","Bell's","Vireo"],\
"Elf_Owl":["Micrathene", "whitneyi", "Elf","Owl"],\
"Gila_Woodpecker":["Melanerpes", "uropygialis","Gila","Woodpecker"],\
"Gilded_Flicker":["Colaptes", "chrysoides","Gilded","Flicker"],\
"Sonoran_Yellow_Warbler":["Setophaga", "petechia", "sonorana","Warbler"],\
"Southwestern_Willow_Flycatcher":["Empidonax", "traillii", "extimus","Willow","Flycatcher"],\
"Summer_Tanager":["Piranga" "rubra","Summer","Tanager"],\
"Vermilion_Flycatcher":["Pyrocephalus", "rubinus","Vermilion","Flycatcher"],\
"Yellow-billed_Cuckoo":["Coccyzus", "americanus", "occidentalis","Yellow-billed","Cuckoo"],\
"California_Black_Rail":["Laterallus","jamaicensis","coturniculus","Rail"],\
"Least_Bittern":["Ixobrychus", "exilis","Bittern"],\
"Yuma_Clapper_Rail":["Rallus", "longirostris", "yumanensis","Clapper","Rail"],\
"Bonytail":["Gila", "elegans","Bonytail"],\
"Flannelmouth_Sucker":["Catostomus", "latipinnis","Flannelmouth","Sucker"],\
"Humpback_Chub":["Gila", "cypha","Humpback","Chub"],\
"Razorback_Sucker":["Xyrauchen", "texanus","Razorback","Sucker"],\
"MacNeill's_Sootywing":["Hesperopsis" "gracielae","MacNeill's","Sootywing"],\
"Western_Red_Bat":["Lasiurus", "blossevillii","Bat"],\
"Western_Yellow_Bat":["Lasiurus", "xanthinus","Bat"],\
"California_Leaf-Nosed_Bat":["Macrotus", "californicus","Leaf-Nosed","Bat"],\
"Townsend's_Big-Eared_Bat":["Corynorhinus","townsendii","Townsend's","Big-Eared","Bat"],\
"Colorado_River_Cotton_Rat":["Sigmodon","arizonae","plenus","Cotton","Rat"],\
"Yuma_Hispid_Cotton_Rat":["Sigmodon","hispidus","eremicus","Hispid","Cotton","Rat"],\
"Desert_Pocket_Mouse":["Chaetodipus","penicillatus","sobrinus","Pocket","Mouse"],\
"Sticky_Buckwheat":["Eriogonum","viscidulum","Sticky","Buckwheat"],\
"Threecorner_Milkvetch":["Astragalus","geyeri", "triquetrus","Threecorner","Milkvetch"],\
"Desert_Tortoise":["Gopherus","agassizii","Desert","Tortoise"],\
"Flat-Tailed_Horned_Lizard":["Phrynosoma","mcalli","Flat-Tailed","Horned","Lizard"]}

#species names
listOfSpecies = ['Gilded Flicker', "Arizona Bell's Vireo", 'Relict Leopard Frog', 'Razorback Sucker', 'Sonoran Yellow Warbler', 'Flannelmouth Sucker', 'Southwestern Willow Flycatcher', 'Vermilion Flycatcher', 'Yuma Clapper Rail', 'Western Red Bat', 'Flat-Tailed Horned Lizard', "MacNeill's Sootywing", 'Yuma Hispid Cotton Rat', 'Threecorner Milkvetch', 'Elf Owl', 'California Black Rail', 'Summer Tanager', 'Gila Woodpecker', 'Yellow-billed Cuckoo','Lowland Leopard Frog', 'Least Bittern', 'Western Yellow Bat', "Townsend's Big-Eared Bat", 'Colorado River Toad', 'Colorado River Cotton Rat', 'Desert Pocket Mouse', 'Humpback Chub', 'California Leaf-Nosed Bat', 'Sticky Buckwheat', 'Desert Tortoise', 'Bonytail']
listOfSpeciesLin = ["Colaptes chrysoides","Vireo bellii arizonae", "Lithobates onca", "Xyrauchen texanus", "Setophaga petechia","Catostomus latipinnis","Empidonax traillii extimus","Pyrocephalus rubinus", "Rallus longirostris yumanensis", "Lasiurus blossevillii","Phrynosoma mcalli","Hesperopsis gracielae", "Sigmodon hispidus eremicus", "Astragalus geyeri triquetrus","Micrathene whitneyi","Laterallus jamaicensis coturniculus","Piranga rubra","Melanerpes uropygialis","Coccyzus americanus occidentalis","Lithobates Rana yavapaiensis","Ixobrychus exilis","Lasiurus xanthinus","Corynorhinus townsendii","Bufo Incilius alvarius","Sigmodon arizonae plenus","Chaetodipus penicillatus sobrinus","Gila cypha","Macrotus californicus","Eriogonum viscidulum","Gopherus agassizii","Gila elegans"]
shortNames = ['Catostomids','Rana','rana','Bufo','bufo','Gilded flicker','Elf owl','California Leaf-nosed Bat','Yellow-Billed Cuckoo','yellow-billed cuckoo','Flat-tailed Horned Lizard','Flycatcher','flycatcher','Sigmodon eremicus','Sigmodon arizonae','Sootywing','Razorback', 'razorback', 'bonytail', 'RASU', 'BONY', 'SWFL', 'Flannelmouth', 'flannelmouth']
nonCoveredSpecies = ["catfish","trout","Trout","Quagga","Striped Bass","Carp","Green Sunfish","Bluegill","Smallmouth Bass","Largemouth Bass","rainbow trout","zooplankton","Zooplankton","Cyprinodon macularius","Moapa Dace","Giant Salvinia","Achii","Achii hanyo","Peregrine_Falcon","Sandhill Crane","Mohave Fringe-toed Lizard","Arrowweed", "arrowweed", "Coyote willow", "Desert broom", "Fremont Cottonwood", "Goodding's willow", "Heliotrope", "Honey Mesquite", "Mule-Fat", "Quailbush", "Willow baccharis", "Saltcedar","Salt Cedar Beetle", "Tamarisk", "Tamarisk Beetle", "Tamarisk Leaf Beetle"]

listOfSpecies = listOfSpecies + nonCoveredSpecies


def addPlurals(listNames, s='s'):
    plural = []
    for name in listNames:
        plural.append(name+s)
    return listNames+plural

listOfSpecies = addPlurals(listOfSpecies)
listOfSpeciesLin = addPlurals(listOfSpeciesLin)
shortNames = addPlurals(shortNames)



#generate list of search terms
#convert dict values into lowercase list
searchWords = list(listedSpecies.values())
searchWords = [item.lower() for sublist in searchWords for item in sublist]
#remove duplicates
searchWords = list(set(searchWords))

#add old search terms
searchWords = searchWords + extraSearchTerms + data_combined


def parsePDF(filename):
    parseList = []
    wordList = []
    
    f = open(filename, 'rb')
    reader = PdfFileReader(f)
    pages = reader.numPages
    docInfo = reader.getDocumentInfo()
    title = docInfo.title 
    print(title)

    titleTags = []

    try:
        #search title for species names
        for speciesName in listOfSpecies+shortNames:
            if speciesName in title and speciesName not in titleTags:
                titleTags.append(speciesName)
    except:
        print('fail species name title search')

    try:
        #search pages for species names        
        for i in range(pages):
            contents = reader.getPage(i).extractText()
            
            for speciesName in listOfSpecies:
                if speciesName in contents and speciesName not in titleTags:
                    titleTags.append(speciesName)  
    except:
        print('fail species name page search')

    try:
        #search title for Scientific names
        for speciesName in listOfSpeciesLin:
            if speciesName in title and speciesName not in titleTags:
                titleTags.append(speciesName)
    except:
        print('fail Scientific name title search')

    try:
        #search pages for Scientific names        
        for i in range(pages):
            contents = reader.getPage(i).extractText()
            
            for speciesName in listOfSpeciesLin:
                if speciesName in contents and speciesName not in titleTags:
                    titleTags.append(speciesName) 
    except:
        print('fail Scientific name page search')


# =============================================================================
#     try:        
#         #parse pdf to create wordList    
#         for i in range(pages):
#             contents = reader.getPage(i).extractText().split(' ')
#                   
#                   
#             for line in contents:
#                 line = line.encode('ascii', 'replace').decode('ascii') #replaces international symbols to get rid of problems with compatibility between unicode and strings
#                 
#                 for word in line.replace('\n', ' ').replace('(', ',').replace(')', ',').replace('{', ',').replace('}',',').replace('[', ',').replace(']',',').replace('"', ',').replace('\\', ',').replace('/', ',').replace('>', ',').replace('<', ',').replace(';', ',').replace('*', ',').replace('&', ',').replace('€', ',').replace('£', ',').replace('$', ',').replace(':', ',').replace('=', ',').replace('?', ',').replace('.', ',').split(','):
#                     word = word.replace(' ','').lower()
#                     word = ''.join([i for i in word if not i.isdigit()]) #strip out numbers
#                     try:
#                         if word[0] == '-':
#                             word = word.replace('-','')                        
#                         
#                         if word[-1] == '-':
#                             word = word.replace('-','')
#                     except:
#                         pass
#                     #word = ''.join([i for i in word])
#                     if len(word) < 20:
#                         parseList.append(word)
#                             
#     except:
#         print('fail page parse')
# 
#     try:    
#         #search wordList for search terms    
#         for word in parseList:
#             if word in searchWords and word not in wordList:
#                 wordList.append(word)
#     except:
#         print('fail wordList search')
# =============================================================================

# =============================================================================
#     nameList = []
# 
#     for name, searchTerms in list(listedSpecies.items()):
# 
#         terms = [item.lower() for item in searchTerms]
#         for word in terms:
#             if word in wordList:
#                 nameList.append(name)
#     
#     if nameList == []:
#         nameList.append("No_Species_Identified")
# 
#     nameCount = Counter(nameList)
#  
#     print(max(nameCount))  
#     #print(max(zip(nameCount.values(), nameCount.keys()))[1])
# =============================================================================
         

    f.close()
    
    if titleTags == []:
        titleTags.append("NoSpeciesName")

# =============================================================================
#     if wordList == []:
#         wordList.append("NoSearchWords")
#         
#     #limit wordList size
#     if len(wordList) > 15:
#         wordList = wordList[0:15]
# =============================================================================
    
    titleTags = " ".join(str(x) for x in titleTags)
# =============================================================================
#     wordList = " ".join(str(x) for x in wordList)
# =============================================================================

    try:
        titleTags = titleTags.replace(' ','_')
        #just in case
        titleTags = titleTags.replace('\n', '_').replace('(', '_').replace(')', '_').replace('{', '_').replace('}','_').replace('[', '_').replace(']','_').replace('"', '_').replace('\\', '_').replace('/', '_').replace('>', '_').replace('<', '_').replace(';', '_').replace('*', '_').replace('&', '_').replace('€', '_').replace('£', '_').replace('$', '_').replace(':', '_').replace('=', '_').replace('?', '_').replace('.', '_')
        titleTags = titleTags.encode('ascii', 'replace').decode('ascii')
     
    except:
        pass

# =============================================================================
#     try:
#         wordList = wordList.replace(' ','_')
#         #just in case
#         wordList = wordList.replace('\n', '_').replace('(', '_').replace(')', '_').replace('{', '_').replace('}','_').replace('[', '_').replace(']','_').replace('"', '_').replace('\\', '_').replace('/', '_').replace('>', '_').replace('<', '_').replace(';', '_').replace('*', '_').replace('&', '_').replace('€', '_').replace('£', '_').replace('$', '_').replace(':', '_').replace('=', '_').replace('?', '_').replace('.', '_')
#         wordList = wordList.encode('ascii', 'replace').decode('ascii')
#      
#     except:
#         pass
# =============================================================================

    try:
        title = title.replace(' ','_')
    except:
        pass
    
    #print (titleTags)
    #print (wordList)
    
    return titleTags, wordList, title

#try 2 times
i = 0
while i < 2:    
    for file in files_in_dir:
        try:
            print(file)
            titleTags, bodyTags, title = parsePDF(os.path.join(path,file))

            #newFileName = titleTags+'--'+bodyTags+'---'+file
            newFileName = titleTags+'---'+title+'---'+file
            resultsPath = os.path.join(path,"results")
            copy2(os.path.join(path,file), os.path.join(resultsPath,newFileName))

        except:
            print('miss')
            resultsPath = os.path.join(path,"results")
            copy2(os.path.join(path,file), os.path.join(resultsPath,file))
            
        i+=1

