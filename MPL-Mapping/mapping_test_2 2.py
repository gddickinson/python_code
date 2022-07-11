# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 20:34:06 2015

@author: george
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines
# you can also have 'l' for low, then 'h' for high. Unless coastlines are
# really important to you, or lakes, you should just use c for crude.
m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='l')
m.drawcoastlines()
m.fillcontinents(color='#072B57',lake_color='#FFFFFF')
# draw parallels and meridians.

m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))

m.drawmapboundary(fill_color='#FFFFFF')
plt.title("Geo Plotting Tutorial")
plt.show()