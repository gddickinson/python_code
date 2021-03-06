from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
fig = plt.figure()
ax = Axes3D(fig)
x = [0,.1,.2,.3]
y = [0,0,0,0]
z = [0,1,1,0]
verts = [list(zip(x, y,z))]
ax.add_collection3d(Poly3DCollection(verts))
plt.show()