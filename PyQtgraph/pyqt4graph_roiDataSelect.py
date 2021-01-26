# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:19:53 2015

@author: robot
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import SimpleCV as simplecv

#==============================================================================
# ## Create image to display
# arr = np.ones((100, 100), dtype=float)
# arr[45:55, 45:55] = 0
# arr[25, :] = 5
# arr[:, 25] = 5
# arr[75, :] = 5
# arr[:, 75] = 5
# arr[50, :] = 10
# arr[:, 50] = 10
# arr += np.sin(np.linspace(0, 20, 100)).reshape(1, 100)
# arr += np.random.normal(size=(100,100))
#==============================================================================
img = simplecv.Image('/home/george2/Pictures/shakespeare.jpg')
arr = img.getNumpy()

## create GUI
app = QtGui.QApplication([])
w = pg.GraphicsWindow(size=(500,400), border=True)
w.setWindowTitle('pyqtgraph example: ROI Examples')

text = """Data Selection From Image.<br>\n
Drag an ROI or its handles to update the selected image.<br>
Hold CTRL while dragging to snap to pixel boundaries<br>
and 15-degree rotation angles.
"""
w1 = w.addLayout(row=0, col=0)
label1 = w1.addLabel(text, row=0, col=0)
v1a = w1.addViewBox(row=1, col=0, lockAspect=True)
v1b = w1.addViewBox(row=2, col=0, lockAspect=True)
img1a = pg.ImageItem(arr)
v1a.addItem(img1a)
img1b = pg.ImageItem()
v1b.addItem(img1b)
v1a.disableAutoRange('xy')
v1b.disableAutoRange('xy')
v1a.autoRange()
v1b.autoRange()

rois = []
rois.append(pg.RectROI([20, 20], [20, 20], pen=(0,9)))
rois[-1].addRotateHandle([1,0], [0.5, 0.5])
#rois.append(pg.LineROI([0, 60], [20, 80], width=5, pen=(1,9)))
#rois.append(pg.MultiRectROI([[20, 90], [50, 60], [60, 90]], width=5, pen=(2,9)))
#rois.append(pg.EllipseROI([60, 10], [30, 20], pen=(3,9)))
#rois.append(pg.CircleROI([80, 50], [20, 20], pen=(4,9)))
#rois.append(pg.LineSegmentROI([[110, 50], [20, 20]], pen=(5,9)))
#rois.append(pg.PolyLineROI([[80, 60], [90, 30], [60, 40]], pen=(6,9), closed=True))


def update(roi):
    img1b.setImage(roi.getArrayRegion(arr, img1a), levels=(0, arr.max()))
    v1b.autoRange()
    
for roi in rois:
    roi.sigRegionChanged.connect(update)
    v1a.addItem(roi)

update(rois[-1])

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()