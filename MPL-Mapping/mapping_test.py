# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 20:27:06 2015

@author: george
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
plt.title("Quick Basemap Example!")
plt.show()