# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 15:32:09 2019

@author: George
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, snd = wavfile.read(r"C:\Users\George\Dropbox\code\JavaScript_HTML_CSS\soundTest\audio\bells_chimes\gong.wav")

snd = snd / (2.**15)
s1 = snd[:,0]

plt.figure(figsize=(20,8))
plt.style.use("seaborn")

time = np.arange(0, s1.shape[0], 1)
time = (time / fs) * 1000

plt.plot(time, s1, color='b')

plt.ylabel('Amplitude', fontsize=16)
plt.xlabel('Time (ms)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.show()



