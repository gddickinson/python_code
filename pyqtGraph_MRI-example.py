"""Test GL volume tool with MRI data."""

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
from nibabel import load

# get MRI data
nii = load(r'C:\Users\George\Desktop\brain\test4d.nii.gz')
#nii = load(r"C:\Users\George\Desktop\brain\T_R_MPRAGE_Axial_0001.img")
data = nii.get_data()
data = np.transpose(data, [2, 0, 1])  # to orient data

# create qtgui
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.orbit(256, 256)
w.setCameraPosition(0, 0, 0)
w.opts['distance'] = 200
w.show()
w.setWindowTitle('pyqtgraph example: GLVolumeItem')

g = gl.GLGridItem()
g.scale(20, 20, 1)
w.addItem(g)

# create color image channels
d2 = np.empty(data.shape + (4,), dtype=np.ubyte)
d2[..., 0] = data * (255./(data.max()/1))
d2[..., 1] = d2[..., 0]
d2[..., 2] = d2[..., 0]
d2[..., 3] = d2[..., 0]
d2[..., 3] = (d2[..., 3].astype(float) / 255.)**2 * 255

# RGB orientation lines (optional)
d2[:, 0, 0] = [255, 0, 0, 255]
d2[0, :, 0] = [0, 255, 0, 255]
d2[0, 0, :] = [0, 0, 255, 255]

v = gl.GLVolumeItem(d2, sliceDensity=1, smooth=False, glOptions='translucent')
v.translate(-d2.shape[0]/2, -d2.shape[1]/2, -150)
w.addItem(v)

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()