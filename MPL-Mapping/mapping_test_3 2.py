# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 20:40:53 2015

@author: george
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


def basicMap():
    m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=90,\
                llcrnrlon=-180,urcrnrlon=180,resolution='c')

    m.drawcoastlines()

    m.drawcountries()
    m.drawstates()


    m.fillcontinents(color='#04BAE3',lake_color='#FFFFFF')

    m.drawmapboundary(fill_color='#FFFFFF')
    plt.title("Geo Plotting Tutorial")
    plt.show()

basicMap()

def coolerProjections():
    m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=90,\
                llcrnrlon=-180,urcrnrlon=180,resolution='c')

    m.drawcountries()
    m.drawstates()


    m.bluemarble()

    plt.title("Geo Plotting Tutorial")
    plt.show()


# are you getting an error like:
# ImportError: The _imaging C module is not installed
# This meanss you have PIL, but you have the wrong bit version.
# If it says you don't have PIL at all, then you better go grab it
# but this should have come with your matplotlib installation.

coolerProjections()