# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 10:41:01 2017

@author: George
"""

from arcgis.gis import GIS
from arcgis.viz import MapView

gis = GIS()
map = MapView()
map.center = gis.tools.geocoder.find_best_match('Redlands, CA')
map