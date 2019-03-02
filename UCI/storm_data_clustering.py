# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 14:48:54 2014

@author: Kyle Ellefsen
Clustering storm data
"""
import numpy as np
from scipy import spatial
from pyqtgraph import plot, show
import pyqtgraph as pg
from random import randint

filename="C:\\Users\\George\\Desktop\\Kyle_Cluster\\storm_XY.txt"
A=np.fromfile(filename,sep=" ")
A=A.reshape((len(A)/2,2))

maxClusterDiameter=100
block_size=10000
A_block=A[(A[:,0]<block_size)*(A[:,1]<block_size),:]
D=spatial.distance_matrix(A_block,A_block)
densities=np.sum((D<maxClusterDiameter),0)-1
densities_jittered=densities+np.arange(len(densities))/np.float(len(densities)) #I do this so no two densities are the same, so each cluster has a peak.

'''
y,x=np.histogram(densities,bins=100)
plot(x[:-1],y,stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))

p=plot()
s1=pg.ScatterPlotItem(size=5, pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 255, 255))
s1.addPoints(x=A_block[:,0],y=A_block[:,1])
p.addItem(s1)

x=[d[0] for d in higher_pts]
y=[d[2] for d in higher_pts]
p=plot(x,y,pen=None, symbol='o')
x=np.arange(0,1000)
p.plot(x,2000/x)
'''
higher_pts=[] #will be a list containing [distance to next highest point, index of next highest point, density of this point]
for pt in np.arange(len(D)):
    d=D[pt,:]
    idx=np.argsort(d)
    i=1
    while densities_jittered[idx[0]]>densities_jittered[idx[i]]:
        i+=1
        if i==len(densities_jittered): #if this is the most dense point, then no point will have a higher density
            higher_pts.append([np.sqrt(2*block_size**2),idx[pt],densities[idx[pt]]])
            break
    if i!=len(densities_jittered): #if this is the most dense point, then no point will have a higher density
        higher_pts.append(np.array([d[idx[i]],idx[i],densities[idx[i]]]))
higher_pts=np.array(higher_pts)

centers=[]
for i in np.arange(len(higher_pts)):
    x=higher_pts[i][0]
    y=higher_pts[i][2]
    if 2000/x<y:#I got this threshold from looking at the scatter plot.  I could also use a combination of the distance to the next point and the density of this point.
        centers.append(i)
        
def get_lower_pts(pt,centers):
    pts=np.argwhere(higher_pts[:,1]==pt).T[0]
    pts=np.array([pt for pt in pts if pt not in centers])
    lower_pts=np.copy(pts)
    for pt in pts:
        lower_pts=np.concatenate((lower_pts,get_lower_pts(pt,centers)))
    return lower_pts

clusters=[]
for pt in centers:
    cluster=np.concatenate((np.array([pt]),get_lower_pts(pt,centers).astype(np.int)))
    clusters.append(cluster)
    
cluster_sizes=np.array([len(c) for c in clusters])
for i in np.arange(len(clusters),0,-1)-1:
    if cluster_sizes[i]<5:  #this constant is arbitrary
        del clusters[i]
        

p=plot()
s1=pg.ScatterPlotItem(size=5, pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 255, 255))
nColors=len(clusters)
for c, cluster in enumerate(clusters):
    color=pg.intColor(c,nColors)
    spots = [{'pos': A_block[cluster[i]], 'brush':color} for i in np.arange(len(cluster))]
    s1.addPoints(spots)
p.addItem(s1)












