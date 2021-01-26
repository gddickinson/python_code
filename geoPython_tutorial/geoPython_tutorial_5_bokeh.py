# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 15:27:25 2020

@author: g_dic
https://automating-gis-processes.github.io/2016/Lesson5-interactive-map-bokeh.html
"""

from bokeh.plotting import figure, save, show

p = figure(title="My first interactive plot!")

# Let's see what it is
p

# Create a list of x-coordinates
x_coords = [0,1,2,3,4]

# Create a list of y-coordinates
y_coords = [5,4,1,2,0]

# Plot the points
p.circle(x=x_coords, y=y_coords, size=10, color="red")

# Give output filepath
outfp = r"C:\Users\g_dic\Documents\geoPython_tutorial\Data\Results\points.html"

# Save the plot by passing the plot -object and output path
save(obj=p, filename=outfp)

show(p)