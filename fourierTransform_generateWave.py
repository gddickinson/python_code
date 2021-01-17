# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:55:37 2019

@author: George
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14

def gen_wave(freq, amp, T, shift, sr):
    #frequency, amplitude, period, phase shift, sampling rate
    
    time = np.arange(0,T,T/sr)
    
    X = amp * np.sin(2 * np.pi * freq * time+shift)
    
    return time,X

#simple signal - single wave
#time, amplitude = gen_wave(1, 1, 1, 0, 1000)
    
#complex signal - multiple waves summed together
time, amplitude1 = gen_wave(1, 1, 10, 1, 1000)    
time, amplitude2 = gen_wave(2, 2, 10, 1, 1000)
time, amplitude3 = gen_wave(3, 4, 10, 0, 1000)


amplitude = amplitude1 + amplitude2 + amplitude3

fig = plt.figure(figsize=(15,5))

ax = fig.add_axes([0, 0, 1, 1])
ax.set_ylim([-7,7])

ax.plot(time, amplitude, c="b")

plt.grid(True, which="both")

plt.show()
