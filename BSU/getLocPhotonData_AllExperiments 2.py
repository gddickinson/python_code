# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:06:06 2019

@author: GEORGEDICKINSON
"""
import pandas as pd
import glob, os
from datetime import date

#get all csv files in folder
path = r"Y:\8_NAM (Nucleic-Acid Memory)_Sep2017_InProgress\11_Super-Resolution\All_Data"
#path = r"Y:\8_NAM (Nucleic-Acid Memory)_Sep2017_InProgress\11_Super-Resolution\Test"
path = r"Y:\8_NAM (Nucleic-Acid Memory)_Sep2017_InProgress\11_Super-Resolution\Missing"

#get all filenames in folder
fileList = [f for f in glob.glob(path + "**/*.csv", recursive=True)]

#remove old resultsTable from list, if present
try:
    fileList.remove(saveName)
except:
    pass


def to_integer(dt_time):
    '''convert date to integer'''
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day



#Lists to store summary stats for pd dataframe
dateList = []
integerDateList = []
filename = []
totalCounts = []
totalPhotons = []
first500Counts = []
first500Photons = []
numberFrames = []
countsPerFrame = []
photonsPerFrame = []
counts500_perFrame = []
photons_500_perFrame = []
averageSigma = []
averageUncertainty = []
averageSigma500 = []
averageUncertainty500 = []
averageBackground = []
averageBackground_500 = []
averageBkgstd = []
averageBkgstd_500 = []
thunderstormVersion = []
averagechi2 = []

i = 0

#start iterating through files
for file in fileList:
    '''iterate through every data file - create summary stats'''
    try:
        #import thunderStorm loc file
        filePath = file        
        name = filePath.split('\\')[-1]          
        #get data
        locs = pd.read_csv(filePath)   
        #see head
        #print(locs.head(n=5))
        #get col names
        colNames = list(locs.columns) 
        
        #get summary data for each experiment for table
        exportName = name.split('_')[0]       
        counts = locs.groupby(['frame']).size().reset_index(name='counts')
        totalNumCounts = counts.sum()['counts']
        counts500 = counts[0:500].sum()['counts'] 
        
        try:
            photons = locs.groupby(['frame']).sum()['intensity [photon]'].reset_index(name='photons')
        except:
            photons = locs.groupby(['frame']).sum()['intensity_photon'].reset_index(name='photons')
        
                
        totalNumPhotons = photons.sum()['photons']
        photons500 = photons[0:500].sum()['photons']        

        numberOfFrames = len(counts)
        
        try:
            sigma = locs.groupby(['frame']).mean()['sigma [nm]'].reset_index(name='sigma')
        except:
            sigma = locs.groupby(['frame']).mean()['sigma_nm'].reset_index(name='sigma')
        
        averageSigmaValue = sigma.mean()['sigma']        
        sigma500 = sigma[0:500].mean()['sigma']  

        try:
            uncertainty = locs.groupby(['frame']).mean()['uncertainty_xy [nm]'].reset_index(name='uncertainty')
        except:
            uncertainty = locs.groupby(['frame']).mean()['uncertainty_xy_nm'].reset_index(name='uncertainty')
            
        averageUncertaintyValue = uncertainty.mean()['uncertainty']   
        uncertainty500 = uncertainty[0:500].mean()['uncertainty']  
        
        try:
            background_STD = locs.groupby(['frame']).mean()['bkgstd [photon]'].reset_index(name='bkgstd')
        except:
            background_STD = locs.groupby(['frame']).mean()['bkgstd_photon'].reset_index(name='bkgstd')
 
        averagebackground_STDValue = background_STD.mean()['bkgstd']        
        background_STD500 = background_STD[0:500].mean()['bkgstd'] 
           
        try:
            background = locs.groupby(['frame']).mean()['offset [photon]'].reset_index(name='background')
        except:
            background = locs.groupby(['frame']).mean()['offset_photon'].reset_index(name='background') 

        averagebackgroundValue = background.mean()['background']        
        background500 = background[0:500].mean()['background'] 
        
        try:
            chi2 = locs.groupby(['frame']).mean()['chi2'].reset_index(name='chi2')
            averagechi2Value = chi2.mean()['chi2']   
        except:
            pass
       
        
    except:
        print('skipped: ', file)
        continue
    
    #if parsed OK append to lists
    excelDate = exportName[0:4] +r'/'+ exportName[4:6] + r'/'+ exportName[6:8]
    
    #try:
    integerDate = to_integer(date(int(exportName[0:4]), int(exportName[4:6]), int(exportName[6:8]))) 
    #except:
    #    integerDate = 99999999999
    
    dateList.append(excelDate) 
    integerDateList.append(integerDate)
    filename.append(name)
    totalCounts.append(totalNumCounts)
    first500Counts.append(counts500)
    totalPhotons.append(totalNumPhotons)
    first500Photons.append(photons500)
    numberFrames.append(numberOfFrames)
    countsPerFrame.append(totalNumCounts/numberOfFrames)
    photonsPerFrame.append(totalNumPhotons/numberOfFrames)    
    counts500_perFrame.append(counts500/500)
    photons_500_perFrame.append(photons500/500)
    averageSigma.append(averageSigmaValue)
    averageUncertainty.append(averageUncertaintyValue)
    averageSigma500.append(sigma500)
    averageUncertainty500.append(uncertainty500)

    averageBackground.append(averagebackgroundValue)
    averageBackground_500.append(background500)
    averageBkgstd.append(averagebackground_STDValue)
    averageBkgstd_500.append(background_STD500)

    
    if 'chi2' in colNames:
        thunderstormVersion.append('1')
        averagechi2.append(averagechi2Value)
    else:
        thunderstormVersion.append('0')
        averagechi2.append('NA')
    
    

    #make dataframe
    d = {'date':dateList,
         'integerDate': integerDateList,
         'name': filename,
         'frames': numberFrames,
         'counts_all':totalCounts,
         'photons_all': totalPhotons,
         'countsPerFrame': countsPerFrame,
         'photonsPerFrame': photonsPerFrame,
         'counts_500': first500Counts,
         'photons_500': first500Photons,
         'counts_500_perFrame': counts500_perFrame,
         'photons_500_perFrame' :photons_500_perFrame,
         'averageSigma': averageSigma,
         'averageUncertainty': averageUncertainty,
         'averageSigma_500': averageSigma500,
         'averageUncertainty_500': averageUncertainty500,      
         'averageBackground':averageBackground,
         'averageBackground_500':averageBackground_500,
         'averageBkgstd':averageBkgstd,
         'averageBkgstd_500':averageBkgstd_500,     
         'thunderstormVersion':thunderstormVersion,   
         'averageChi2': averagechi2
         
         }
    
    summaryDF = pd.DataFrame(data=d)     
    
    #save intermediate results as table
    if i%10 == 0:
        saveName = os.path.join(path,'summaryTable_{}.csv'.format(i))
        summaryDF.to_csv(saveName)
        print(i, ': table saved to: ', saveName)
    i += 1


#save final table
saveName = os.path.join(path,'summaryTable3.csv')
summaryDF.to_csv(saveName)
print(i, ': table saved to: ', saveName)
print('finished')

