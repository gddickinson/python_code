# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 17:20:51 2015

@author: george
"""

import sys

if sys.version_info[:2]<(2,5):
    def partial(func,arg):
        def callme():
            return func(arg)
        return callme
else:
    from functools import partial

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form,self).__init__(parent)
        button1 = QPushButton("One")
        button2 = QPushButton("Two")
        self.connect(button1,SIGNAL("clicked()"),self.one)
        self.connect(button2,SIGNAL("clicked()"),partial(self.anyButton,"Two"))
 
        grid =QGridLayout()
        grid.addWidget(button1, 0,0)
        grid.addWidget(button2, 0,1)
        self.setLayout(grid)



   
    def one(self):
        self.label.setText("You clicked button 'One'")

    def anyButton(self, who):
        self.label.setText("You clicked button '%s" % who)
    


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()