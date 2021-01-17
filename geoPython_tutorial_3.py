# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:04:06 2020

@author: g_dic
https://automating-gis-processes.github.io/2016/Lesson3-geocoding.html
"""

#Geocoding in Geopandas

# Import necessary modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
#import googlemaps
#from datetime import datetime

# Filepath
fp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\addresses.txt"

# Read the data
data = pd.read_csv(fp, sep=';')

# Let's take a look of the data
data.head()

# Import the geocoding tool
from geopandas.tools import geocode

# Key for our Google Geocoding API (NEED TO SET UP OWN PROJECT AND KEY FOR THIS)
# Notice: only the cloud computers of our course can access and
# successfully execute the following
#key = 'AIzaSyCyfUQFAMS7JhNYt3-s5ff48-Fb0_SQJJc'
#gmaps = googlemaps.Client(key=key)
# Geocode addresses
#geo = gmaps.geocode(data['address'])

#Using geopandas geocoding tool instead of Google
geo = gpd.tools.geocode(data['address'])

geo.head(2)

#Table joins
# Join tables by using a key column 'address'
join = geo.merge(data, on='address')

# Let's see what we have
join.head()

type(join)

# Output file path
outfp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\Results\addresses.shp"

# Save to Shapefile
join.to_file(outfp)

#plot
join.plot();

#Reprojecting data
import geopandas as gpd

# Filepath to the addresses Shapefile
fp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\Results\addresses.shp"

# Read data
data = gpd.read_file(fp)

#Check crs
data.crs

data['geometry'].head()

# Let's take a copy of our layer
data_proj = data.copy()

# Reproject the geometries by replacing the values with projected ones
data_proj['geometry'] = data_proj['geometry'].to_crs(epsg=3879)


data_proj['geometry'].head()


import matplotlib.pyplot as plt

# Plot the WGS84
data.plot(markersize=6, color="red");

# Add title
plt.title("WGS84 projection");

# Remove empty white space around the plot
plt.tight_layout()

# Plot the one with ETRS GK-25 projection
data_proj.plot(markersize=6, color="blue");

# Add title
plt.title("ETRS GK-25 projection");

# Remove empty white space around the plot
plt.tight_layout()


from fiona.crs import from_epsg

# Determine the CRS of the GeoDataFrame
data_proj.crs = from_epsg(3879)

# Let's see what we have
data_proj.crs

# Pass the coordinate information
data_proj.crs = {'y_0': 0, 'no_defs': True, 'x_0': 25500000, 'k': 1, 'lat_0': 0, 'units': 'm', 'lon_0': 25, 'ellps': 'GRS80', 'proj': 'tmerc'}

# Check that it changed
data_proj.crs

# Ouput file path
outfp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\Results\addresses_epsg3879.shp"

# Save to disk
data_proj.to_file(outfp)


#Check if point is inside a polygon
from shapely.geometry import Point, Polygon

# Create Point objects
p1 = Point(24.952242, 60.1696017)
p2 = Point(24.976567, 60.1612500)

# Create a Polygon
coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
poly = Polygon(coords)

print(p1)
print(p2)
print(poly)

# Check if p1 is within the polygon using the within function
p1.within(poly)
# Check if p2 is within the polygon
p2.within(poly)

# Our point
print(p1)
# The centroid
print(poly.centroid)

# Does polygon contain p1?
poly.contains(p1)

# Does polygon contain p2?
poly.contains(p2)

#Intersect
from shapely.geometry import LineString, MultiLineString

# Create two lines
line_a = LineString([(0, 0), (1, 1)])
line_b = LineString([(1, 1), (0, 2)])

#Do they intersect?
line_a.intersects(line_b)
#Do they touch
line_a.touches(line_b)

# Create a MultiLineString
multi_line = MultiLineString([line_a, line_b])

multi_line















