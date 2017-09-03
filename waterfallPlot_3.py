from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy

fileName = r"C:\Users\George\Desktop\US_elevation_profiles\state_EW_elevation_profiles_1000points.txt"

df= pd.read_table(fileName, index_col =0)

#make deepcopy otherwise sort array also sorts df
array = copy.deepcopy(df.iloc[:,0:].values)

array.sort(axis=1)

vertsL = []


for i in range(len(df.columns)):
    z = array[:,i]
    z = np.concatenate([[0],z,[0]])
    x = range(len(z))
    y = [i] * len(z)
    verts = [list(zip(x, y, z))]
    
    vertsL.append(verts)


fig = plt.figure()
ax = Axes3D(fig)

plt.ylim([0,len(vertsL)])
plt.xlim([0,1000])
ax.set_zlim([0,4000])

cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.3)

for i in range(len(vertsL)):
    ax.add_collection3d(Poly3DCollection(vertsL[i], facecolors=[cc('g')]))


plt.show()