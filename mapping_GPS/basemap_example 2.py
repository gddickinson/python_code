# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:18:57 2018

@author: George
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import json
from urllib.request import urlopen
from geopy.geocoders import Nominatim


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

pcLocation = (pcLong,pcLat)

#city locations
geolocator = Nominatim()

def getLoc(location):
    ans = geolocator.geocode(location)
    return (ans[-1])

austin = getLoc("Austin, TX")
washington = getLoc("Washington, DC")
chicago = getLoc("Chicago, IL")
losangeles = getLoc("Los Angeles, CA")
philadelphia= getLoc("Philadelphia, PA")
newyork= getLoc("New York, NY")
sanfrancisco= getLoc("San Francisco, CA")

#m = Basemap(projection = 'merc', llcrnrlat=10, urcrnrlat=50,
#        llcrnrlon=-160, urcrnrlon=-60)

# create polar stereographic Basemap instance.


# Lambert Conformal map of lower 48 states.
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=33,lat_2=45,lon_0=-95)


m.drawcoastlines()
m.fillcontinents (color='lightgray', lake_color='lightblue')
m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua')

m.drawcounties()
m.drawstates()


x, y = m(*zip(*[austin, washington, chicago, losangeles, pcLocation]))
#x, y = m(*zip(*[pcLocation]))
m.plot(x,y, marker ='o', markersize=6, markerfacecolor='red', linewidth=0)

plt.title('Mercator Projection')
plt.show()