# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:55:37 2019

@author: George
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from numpy.fft import fft

plt.style.use("seaborn")
plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14

f, axarr = plt.subplots(2, figsize=(20,8)) 

def gen_wave(freq, amp, T, shift, sr):
    #frequency, amplitude, period, phase shift, sampling rate
    
    time = np.arange(0,T,T/sr)
    
    X = amp * np.sin(2 * np.pi * freq * time+shift)
    
    return time,X

#sampling rate
sr = 250 #in HZ

#simple signal - single wave
#x,y = gen_wave(1, 1, 1, 0, sr)
    
#complex signal - multiple waves summed together
x,y = gen_wave(1, 1, 10, 0, sr)    
_,y2 = gen_wave(2, 2, 10, 0, sr)
_,y3 = gen_wave(3, 4, 10, 0, sr)


y = y + y2 + y3

axarr[0].plot(x,y)

n = len(y)
p = fft(y) #this can be slow to run

mag = np.sqrt(p.real**2 + p.imag**2)

mag = mag * 2 / n

#The number of bins = the number of frequencies detectable = the sampling rate
#The spectrogram is symetrical around the Nyquist point so only plotting the first half
mag = mag[0:math.ceil((n)/2.0)] #uncomment to see full spectrogram

x = np.arange(0, len(mag), 1.0) * (sr / n)

threshold = 0

if threshold != 0:
    print(np.unique(np.rint(x[np.in1d(mag, mag[mag>threshold])])), "Hz")
    mag[mag<threshold]=threshold
 
axarr[1].bar(x, mag, color='b')
axarr[1].xaxis.set_ticks(np.arange(min(x),max(x)+1, 1.0))    
  
    
#plt.figure(figsize=(20,8))
#plt.plot(freq/1000, mag, color='b')
#plt.ylabel('Amplitude', fontsize=16)
#plt.xlabel('Frequency (MHz)', fontsize=16)
plt.show()

