# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 13:20:20 2020

@author: g_dic
https://automating-gis-processes.github.io/2016/Lesson2-geopandas-basics.html
"""

# Import necessary modules
import geopandas as gpd

# Set filepath (fix path relative to yours)
fp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\DAMSELFISH_distributions.shp"

# Read shapefile using gpd.read_file()
data = gpd.read_file(fp)

print(type(data))

#table head
data.head()

#simple plotting
data.plot();

#coordinate reference system
data.crs

#write a new shapefile
# Create a output path for the data
out = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\DAMSELFISH_distributions_SELECTION.shp"

# Select first 50 rows
selection = data[0:50]

# Write those rows into a new Shapefile (the default output file format is Shapefile)
selection.to_file(out)

#plot
selection.plot();

# It is possible to use only specific columns by specifying the column name within square brackets []
data['geometry'].head()


# Make a selection that contains only the first five rows
selection = data[0:5]

#We can iterate over the selected rows using a specific .iterrows() -function in (geo)pandas
for index, row in selection.iterrows():
    poly_area = row['geometry'].area
    print("Polygon area at index {0} is: {1:.3f}".format(index, poly_area))

# Empty column for area
data['area'] = None

# Iterate rows one at the time
for index, row in data.iterrows():
    # Update the value in 'area' column with area information at index
    data.loc[index, 'area'] = row['geometry'].area

data['area'].head(2)

# Maximum area
max_area = data['area'].max()

# Minimum area
min_area = data['area'].mean()

print("Max area: %s\nMean area: %s" % (round(max_area, 2), round(min_area, 2)))


#Creating geometries into a GeoDataFrame
# Import necessary modules first
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import fiona

# Create an empty geopandas GeoDataFrame
newdata = gpd.GeoDataFrame()

newdata

# Create a new column called 'geometry' to the GeoDataFrame
newdata['geometry'] = None

# Coordinates of the Helsinki Senate square in Decimal Degrees
coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]

# Create a Shapely polygon from the coordinate-tuple list
poly = Polygon(coordinates)

# Let's see what we have
poly

# Insert the polygon into 'geometry' -column at index 0
newdata.loc[0, 'geometry'] = poly

# Let's see what we have now
newdata

# Add a new column and insert data
newdata.loc[0, 'Location'] = 'Senaatintori'

# Let's check the data
newdata

# Import specific function 'from_epsg' from fiona module to add CRS
from fiona.crs import from_epsg

# Set the GeoDataFrame's coordinate system to WGS84 (epsg code: 4326)
newdata.crs = from_epsg(4326)

# Let's see how the crs definition looks like
newdata.crs

# Determine the output path for the Shapefile
outfp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\Senaatintori.shp"

# Write the data into that Shapefile
newdata.to_file(out)

#Grouping data
data = gpd.read_file(fp)

#list columns
#for col in data.columns: 
#    print(col)

# Group the data by column 'binomial'
grouped = data.groupby('BINOMIAL')

# Let's see what we got
grouped

# Iterate over the group object
for key, values in grouped:
    individual_fish = values

individual_fish

type(individual_fish)
print(key)

# Determine outputpath
outFolder = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data"

# Create a new folder called 'Results' (if does not exist) to that folder using os.makedirs() function
import os
resultFolder = os.path.join(outFolder, 'Results')
if not os.path.exists(resultFolder):
    os.makedirs(resultFolder)


# Iterate over the
for key, values in grouped:
    # Format the filename (replace spaces with underscores)
    outName = "%s.shp" % key.replace(" ", "_")

    # Print some information for the user
    print("Processing: %s" % key)

    # Create an output path
    outpath = os.path.join(resultFolder, outName)

    # Export the data
    values.to_file(outpath)