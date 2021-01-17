# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:56:55 2020

@author: g_dic
"""


import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq 
from matplotlib import pyplot as plt
import os

### PARAMETERS ###
filename = r"C:\Users\g_dic\OneDrive\Desktop\testing\epp_Amplitudes.csv"
chunk_size = 128
time_step = 1 #seconds

# =============================================================================
####fake signal to test
# np.random.seed(1234)
# time_step = 0.02
# period = 5.
# time_vec = np.arange(0, 20, time_step)
# sig = (np.sin(2 * np.pi / period * time_vec) + 0.5 * np.random.randn(time_vec.size))
# =============================================================================


#chunking fft function
def fft_chunks(l, n):
    '''

    Parameters
    ----------
    l : TYPE
        list of numbers.
    n : TYPE
        chunk size.

    Returns
    ------
    TYPE
        dict of lists with fft, power and frequency (Hz) for each quck

    '''
      
    # looping till length l 
    df = pd.DataFrame()
    chunk_num = 1
    
    for i in range(0, len(l), n):
        chunk = l[i:i + n]
        fft_chunk = fft(chunk)
        power_chunk = np.abs(fft_chunk) 
        freq_chunk = fftfreq(chunk.size, d=time_step)
        name1='power_{}'.format(chunk_num)
        name2='frequency_{}'.format(chunk_num)
        d= {name1: power_chunk, name2: freq_chunk}
        newDF = pd.DataFrame(data=d)
        df = pd.concat([df,newDF], axis=1)
        chunk_num += 1
          
    return df

#import trace/traces
data = pd.read_csv(filename, header = None)
columns = list(data) 


#initiate result dict (for multiple traces)
result_dict = {}

#fft analysis
for i in columns:   
    # analyse each column
    result = (fft_chunks(data[i].to_numpy(),chunk_size)) 
    #result = (fft_chunks(sig,chunk_size)) # FOR TESTING     
    # add to result_dict
    result_dict.update( {i : result} )

    
#export results
savePath = os.path.dirname(filename)

for key in result_dict:  
    saveName = os.path.join(savePath,'result_{}.csv'.format(str(key)))
    result_dict[key].to_csv(saveName)
    print('File {} saved'.format(saveName))
    
    
    

### plot test result
test = result_dict[0]
plt.scatter(test['frequency_2'],test['power_2'])


