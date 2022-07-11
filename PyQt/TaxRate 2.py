# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 11:06:20 2015

@author: george
"""

from PyQt4.QtCore import *

class TaxRate(QObject):
    
    def __init__(self):
        super(TaxRate, self).__init__()
        self.__rate = 17.5
        
    def rate(self):
        return self.__rate

    def setRate(self, rate):
        if rate != self.__rate:
            self.__rate = rate
            self.emit(SIGNAL("rateChanged"),self.__rate)
        
def rateChanged(value):
    print "TaxRate changed to %.2f%%" %value


vat = TaxRate()

vat.connect(vat,SIGNAL("rateChanged"),rateChanged)
vat.setRate(17.5)
vat.setRate(8.5)