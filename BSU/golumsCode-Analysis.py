# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:26:59 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
from matplotlib import pyplot as plt
from ast import literal_eval
from itertools import permutations
import numpy as np
import glob

#filePath = r"Y:\George_D_DATA\2019-10-15_Run3-resample_1\20191015_driftCorrected_bin_5860_3000_decoded_p_1_tw_2_e_7_false_positive_ior.csv"
#filePath =r"C:\Users\georgedickinson\Desktop\newAnalysis-GOLAM\2020-02-03_20191015_driftCorrected_bin_5860_RUN3_ior_9error_1FP.csv"
#filePath =r"C:\Users\georgedickinson\Desktop\golamsCode\Results_02-12-2020\9errors_0FP\20190913_10_38_52_RUN2_decode_ior.csv"


path = r"C:\Users\georgedickinson\Desktop\golamsCode\Results_02-12-2020\9errors_0FP\"

files = [f for f in glob.glob(path + "**/*.csv", recursive=True)]

for filePath in files[0]:

    filePath = r"C:\Users\georgedickinson\Desktop\golamsCode\Results_02-12-2020\9errors_0FP\20190913_10_38_52_RUN3_decode_ior.csv"
    
    #open result csv file as DF
    
    results = pd.read_csv(filePath, dtype={'Line number in file':int, ' origami':str, 'status':int, 'error':int, 'error location':object,
           'orientation':int, 'decoded index':int, 'decoded origami':str, ' decoded data':str,
           'decoding time':float})
    
    #check header names etc
    headers = results.dtypes.index
    print(headers)
    print(results.shape)
    print(results.head(n=5))
    
    origamiDict = {
                    0 :  '001101101111011100111010001101111101111000101010',
                    1 :  '001001101010100110110100000111011111110000000001',
                    2 :  '010111111101100100011100101111001110010000010111',
                    3 :  '001000011000010110011110100100011110001000011010',
                    4 :  '000110101111101100111110000100001101100010010010',
                    5 :  '010111111101010110111000001010011100001010110100',
                    6 :  '000100001110101100011010111000111000011010100101',
                    7 :  '010101001010000111100000110110001101100010000100',
                    8 :  '001000001011111101000100010100111110010001100101',
                    9 :  '001000001101101110101100000100111101000001111101',
                    10 : '011011101101010100000110110111101111110001101000',
                    11 : '000100011110011110011010100000001010111001010100',
                    12 : '010011101100110101000100000000011100010011011000',
                    13 : '010100101001111111001100010100111100111011011011',
                    14 : '000010101101010101101100100010111001010011101111',
                    15 : 'NO'
                   }
    
     
    originalList = []
    
    for i in range(len(results)):
        x = origamiDict[results['decoded index'][int(i)]]
        #print(x)
        originalList.append(x)
    
    
    results['origamiOriginal'] = originalList
    
    results['is decoded'] = (results['decoded origami'] == results['origamiOriginal'])
    
    print(results['decoded index'][0])
    print(results[' origami'][0])
    print(results['decoded origami'][0])
    print(results['origamiOriginal'][0])
    print(results['is decoded'][0])
    
    ##Uncomment to save
    savePath = filePath.split('.')[0] + '_TEST.csv'
    results.to_csv(savePath, header=True, index=True)
    print('Test saved!')
    
    
    errorList = []
    
    def convertStr2Tuple(string):
        if len(string) < 2:
            return ()
        a = string.replace('  ',',')
        b = literal_eval(a)
        return b
        
    for i in range(len(results)):
        errorList.append(convertStr2Tuple(results['error location'][i]))
        
        
    results['error location'] = errorList 
      
    def listPermutations(list1, list2): 
        return [(i,j) for i in list1 for j in list2]
      
    errorCombinations =  listPermutations([0,1,2,3,4,5],[0,1,2,3,4,5,6,7]) 
    
    #errorDict = {v: k for v, k in enumerate(errorCombinations)}
    
    allErrorList = []
    
    #allErrorList.append(errorCombinations)
    
    for i in range(len(results)):
        errorResults = []
        for error in errorCombinations:
            errorResults.append(results['error location'][i].count(error))
        allErrorList.append(errorResults)
    
    allErrorList_arr = np.array(allErrorList)   
    
    errorDF = pd.DataFrame(allErrorList_arr, columns=(errorCombinations))
    
    finalDF = results.join(errorDF) 
    
    #Uncomment to save
    savePath = filePath.split('.')[0] + '_FINAL.csv'
    finalDF.to_csv(savePath, header=True, index=True)
    print('Final saved!')

