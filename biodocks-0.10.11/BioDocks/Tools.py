"""
@author: Brett Settle
@Department: UCI Neurobiology and Behavioral Science
@Lab: Parker Lab
@Date: August 6, 2015
"""
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import difflib

from BioDocks.io import *
from BioDocks.Widgets.SettingsWidgets import *

item_name = ""

def copy(item, name):
    global item_name
    item_name = name
    QtGui.QApplication.clipboard().setText("%s" % asStr(item))

def calculate_distances(arr, maximum = -1):
	dists = []
	for i, p1 in enumerate(arr):
		for p2 in arr[i+1:]:
			d = np.linalg.norm(np.subtract(p1,p2))
			if maximum < 0 or d <= maximum:
				dists.append(d)
	return dists

def sort_closest(lst, close_to=''):
    return sorted(lst, key=lambda i: -difflib.SequenceMatcher(None, i, close_to).ratio())

class AnalysisException(Exception):
    def __init__(self, parent, title='Analysis Error', s='Something went wrong'):
        super(AnalysisException, self).__init__(s)
        QtGui.QMessageBox.critical(parent, message, title)

def showMessage(parent, title, message):
	QtGui.QMessageBox.information(parent, title, message)

def random_color(high = 255, low=0):
    r, g, b = np.random.random((3,))

    return QtGui.QColor(int(r * high) + low, int(g * high) + low, int(b * high) + low)

def getOption(parent, title, options, label='Option:'):
	result, ok = QtGui.QInputDialog.getItem(parent, title, label, options, editable=False)
	assert ok, "Selection Canceled"
	return str(result)

def getString(parent, title="Please enter a string", label="String:", initial=""):
	s, ok = QtGui.QInputDialog.getText(parent, title, label, text=initial)
	assert ok, 'Action canceled'
	return str(s)

def getInt(parent, title="Please enter an integer", label="Value:", initial=0):
	v, ok = QtGui.QInputDialog.getInt(parent, title, label, value=initial)
	assert ok, "Action canceled"
	return int(v)

def getFloat(parent, title="Please enter an integer", label="Value:", initial=0):
	v, ok = QtGui.QInputDialog.getDouble(parent, title, label, value=initial)
	assert ok, "Action canceled"
	return float(v)

def asStr(obj):
	if isinstance(obj, np.ndarray):
		return str(obj.tolist())
	else:
		return repr(obj)

def getArea(points):
        a = 0
        ox,oy = points[0]
        for x,y in points[1:]:
            a += (x*oy-y*ox)
            ox,oy = x,y
        return abs(a/2)

#volume of polygon poly
def volume(poly):
    if len(poly) < 3: # not a plane - no volume
        return 0

    def dot(a, b):
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

    def cross(a, b):
        x = a[1] * b[2] - a[2] * b[1]
        y = a[2] * b[0] - a[0] * b[2]
        z = a[0] * b[1] - a[1] * b[0]
        return (x, y, z)

    def unit_normal(a, b, c):
        def det(a):
            return a[0][0]*a[1][1]*a[2][2] + a[0][1]*a[1][2]*a[2][0] + a[0][2]*a[1][0]*a[2][1] - a[0][2]*a[1][1]*a[2][0] - a[0][1]*a[1][0]*a[2][2] - a[0][0]*a[1][2]*a[2][1]

        x = det([[1,a[1],a[2]],
                 [1,b[1],b[2]],
                 [1,c[1],c[2]]])
        y = det([[a[0],1,a[2]],
                 [b[0],1,b[2]],
                 [c[0],1,c[2]]])
        z = det([[a[0],a[1],1],
                 [b[0],b[1],1],
                 [c[0],c[1],1]])
        magnitude = (x**2 + y**2 + z**2)**.5
        return (x/magnitude, y/magnitude, z/magnitude)

    total = [0, 0, 0]
    for i in range(len(poly)):
        vi1 = poly[i]
        if i is len(poly)-1:
            vi2 = poly[0]
        else:
            vi2 = poly[i+1]
        prod = cross(vi1, vi2)
        total[0] += prod[0]
        total[1] += prod[1]
        total[2] += prod[2]
    result = dot(total, unit_normal(poly[0], poly[1], poly[2]))
    return abs(result/2)
