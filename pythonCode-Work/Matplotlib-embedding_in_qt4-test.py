#!/usr/bin/env python

# embedding_in_qt4.py --- Simple Qt4 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

from __future__ import (absolute_import, division,print_function, unicode_literals)
import sys
import os
import random
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore
import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.cm as cm
import matplotlib.pyplot as plt


progname = os.path.basename(sys.argv[0])
progversion = "0.1"

######## Set filenammes & variables ###########################################
testImage = 'C:\\Users\\George\\Desktop\\arabidopsis.tif'
imageName  = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150717\\150717_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash-ER_before_calcium-imaging_average.tif'
#imageName  = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150717\\150717_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash-ER_before_calcium-imaging_average_divided-by-low-pass.tif'
puffFileName = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150717\\150717_cos_celllights-er-rfp_5umcal520_1umip3_1umegta_uv-flash-calcium-imaging_FLIKA_XY.txt'
STORMFileName = 'J:\\WORK\\STORM_After-Cellights-and-Calcium-Imaging\\COS-CellLights-Red_ER\\150717\\150717_Cos_STORM_IP3R1-NTerm-A405-A647_test2_filtered-5in100.txt'

scaleFactor = 2 ##for FLIKA performed with pixel bining
scaleFactor2 = 160  ##160 nm / pixel

####### Plot Image ############################################################

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


#class MyStaticMplCanvas(MyMplCanvas):
#    """Simple canvas with a sine plot."""
#    def compute_initial_figure(self):
#        t = arange(0.0, 3.0, 0.01)
#        s = sin(2*pi*t)
#        self.axes.plot(t, s)

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        im = plt.imread(testImage)
        #implot = plt.imshow(im, cmap=cm.Greys_r, interpolation = 'nearest')

        self.plt.imshow(im, cmap=cm.Greys_r, interpolation = 'nearest')






class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About",
"""embedding_in_qt4.py example
Copyright 2005 Florent Rougon, 2006 Darren Dale

This program is a simple example of a Qt4 application embedding matplotlib
canvases.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation."""
)


qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
