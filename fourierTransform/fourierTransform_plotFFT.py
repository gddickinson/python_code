# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 15:32:09 2019

@author: George
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import math
from numpy.fft import fft

plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14
plt.style.use("seaborn")


fs, snd = wavfile.read(r"C:\Users\George\Dropbox\code\JavaScript_HTML_CSS\soundTest\audio\bells_chimes\gong.wav")
y = snd[:,0]

n = len(y)
p = fft(y) #this can be slow to run

mag = np.sqrt(p.real**2 + p.imag**2)

mag = mag * 2 / n

mag = mag[0:math.ceil((n)/2.0)]

freq = np.arange(0, len(mag), 1.0) * (fs / n)

threshold = 400

if threshold != 0:
    print(np.unique(np.rint(freq[np.in1d(mag, mag[mag>threshold])])), "Hz")
    mag[mag<threshold]=threshold
    
plt.figure(figsize=(20,8))
plt.plot(freq/1000, mag, color='b')
plt.ylabel('Amplitude', fontsize=16)
plt.xlabel('Frequency (MHz)', fontsize=16)
plt.show()



