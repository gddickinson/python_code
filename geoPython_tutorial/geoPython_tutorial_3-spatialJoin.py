# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:58:49 2020

@author: g_dic
https://automating-gis-processes.github.io/2016/Lesson3-spatial-join.html
"""

import geopandas as gpd

# Filepath
fp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\Vaestotietoruudukko_2015"

# Read the data
pop = gpd.read_file(fp)

# See the first rows
pop.head()

# Change the name of a column
pop = pop.rename(columns={'ASUKKAITA': 'pop15'})

pop.columns

# Columns that will be sected
selected_cols = ['pop15', 'geometry']

# Select those columns
pop = pop[selected_cols]

# Let's see the last 2 rows
pop.tail(2)

# Addresses filpath
addr_fp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\Results\addresses_epsg3879.shp"

# Read data
addresses = gpd.read_file(addr_fp)

# Check the head of the file
addresses.head(2)


# Check the crs of address points
print(addresses.crs)

# Check the crs of population layer
print(pop.crs)

addresses.crs == pop.crs

# Make a spatial join
join = gpd.sjoin(addresses, pop, how="inner", op="within")

# Let's check the result
join.head()

# Output path
outfp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\Results\addresses_pop15_epsg3979.shp"

# Save to disk
join.to_file(outfp)


import matplotlib.pyplot as plt

# Plot the points with population info
join.plot(column='pop15', cmap="Reds", markersize=7, scheme='natural_breaks', legend=True);

# Add title
plt.title("Amount of inhabitants living close the the point");

# Remove white space around the figure
plt.tight_layout()