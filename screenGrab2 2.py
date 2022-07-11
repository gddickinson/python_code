# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 18:27:39 2015

@author: george
"""

import sys
from PyQt4.QtGui import *

filename = '/home/george/Pictures/Screenshot.jpg'
app = QApplication(sys.argv)
widget = QWidget()
widget.setLayout(QVBoxLayout())
label = QLabel()
widget.layout().addWidget(label)

def take_screenshot():
    p = QPixmap.grabWindow(widget.winId())
    p.save(filename, 'jpg')

widget.layout().addWidget(QPushButton('take screenshot', clicked=take_screenshot))
widget.show()
app.exec_()