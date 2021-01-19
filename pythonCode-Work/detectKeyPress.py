# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 09:23:38 2015

@author: George
"""

try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
 
print ("Press Y or N to continue")
while True:
    char = getch()
    if char.lower() in ("y", "n"):
        print (char)
        break