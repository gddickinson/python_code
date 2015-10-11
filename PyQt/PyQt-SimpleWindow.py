#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we create a simple
window in PyQt4.

author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys
from PyQt4 import QtGui


def main():
    
#==============================================================================
#    Every PyQt4 application must create an application object.
#    The application object is located in the QtGui module. 
#    The sys.argv parameter is a list of arguments from the command line. 
#    Python scripts can be run from the shell. 
#    It is a way how we can control the startup of our scripts.
#==============================================================================
    app = QtGui.QApplication(sys.argv)
    
#==============================================================================
#     The QtGui.QWidget widget is the base class of all user interface objects in PyQt4. We provide the default constructor for QtGui.QWidget. The default constructor has no parent. 
#     A widget with no parent is called a window.
#==============================================================================
    
    w = QtGui.QWidget()
    
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
#==============================================================================
#     Finally, we enter the mainloop of the application.
#     The event handling starts from this point.
#     The mainloop receives events from the window system and dispatches them to the application widgets.
#     The mainloop ends if we call the exit() method or the main widget is destroyed.
#     The sys.exit() method ensures a clean exit.
#     The environment will be informed how the application ended.
#     The exec_() method has an underscore.
#     It is because the exec is a Python keyword.
#     And thus, exec_() was used instead.    
#==============================================================================
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()