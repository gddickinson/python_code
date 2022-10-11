#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:13:49 2022

@author: george
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
%matplotlib qt 


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
t = [0,1,2,3,4,5,6,7,8,9,10]
x = [0,0,0,0,0,0,0,0,0,0]
y = [1,2,3,4,5,6,7,8,9,10]

plt.scatter(x[0], y[0])

axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

ax.set_xlim(-10,10)
ax.set_ylim(-10,10)

spos = Slider(axpos, 't', 0, len(t))

def update(val):
    ax.cla()
    ind = int(spos.val)
    ax.scatter(x[ind], y[ind])
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)
    fig.canvas.draw_idle()

spos.on_changed(update)

plt.show()