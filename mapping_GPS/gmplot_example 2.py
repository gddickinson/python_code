# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 12:30:21 2018

@author: George
"""

import gmplot
import webbrowser
import json
from urllib.request import urlopen

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)

IP=data['ip']
org=data['org']
city = data['city']
country=data['country']
region=data['region']
lat,long = data['loc'].split(',')
#print ('IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,country,city,IP))

pcLat = float(lat)
pcLong = float(long)

zoom = 8

gmap = gmplot.GoogleMapPlotter(pcLat, pcLong, zoom)

#gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
#gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
#gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
#gmap.heatmap(heat_lats, heat_lngs)

gmap.draw("mymap.html")
#webbrowser.open_new_tab("mymap.html")
webbrowser.open("mymap.html")
