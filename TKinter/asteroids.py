# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 08:32:15 2016

@author: george
"""
from turtle import *
import tkinter.messagebox
import tkinter
import random
import math

screenMinX,screenMinY, screenMaxX,screenMaxY = -500, -500, 500, 500


# Start by creating a RawTurtle object for the window. 
root = tkinter.Tk()
root.title("Asteroids!")
cv = ScrolledCanvas(root,600,600,600,600)
cv.pack(side = tkinter.LEFT)
t = RawTurtle(cv)
screen = t.getscreen()
screen.setworldcoordinates(screenMinX,screenMinY, screenMaxX,screenMaxY)
screen.register_shape("rock3",((-20, -16),(-21, 0),(-20,18),(0,27),(17,15),(25,0),(16,-15),(0,-21)))
screen.register_shape("rock2",((-15, -10),(-16, 0),(-13,12),(0,19),(12,10),(20,0),(12,-10),(0,-13)))
screen.register_shape("rock1",((-10,-5),(-12,0),(-8,8),(0,13),(8,6),(14,0),(12,0),(8,-6),(0,-7)))
screen.register_shape("ship",((-10,-10),(0,-5),(10,-10),(0,10)))
screen.register_shape("bullet",((-2,-4),(-2,4),(2,4),(2,-4)))
frame = tkinter.Frame(root)
frame.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)
t.ht()

def quitHandler():
      root.destroy()
      root.quit()

quitButton = tkinter.Button(frame, text = "Quit", \
      command=quitHandler)
quitButton.pack()

ship = SpaceShip(cv,0,0,(screenMaxX-screenMinX)/2+screenMinX, (screenMaxY-screenMinY)/2 + screenMinY)

self.color("#ffff00")
 
asteroids = []
         
for k in range(5):
  dx = random.random() * 6 - 3
  dy = random.random() * 6 - 3
  x = random.random() * (screenMaxX - screenMinX) + screenMinX
  y = random.random() * (screenMaxY - screenMinY) + screenMinY

asteroid = Asteroid(cv,dx,dy,x,y,3)
asteroids.append(asteroid)

def play():
  # Tell all the elements of the game to move
  ship.move()

  for asteroid in asteroids:
    asteroid.move()
  # Set the timer to go off again in 5 milliseconds
  screen.ontimer(play, 5)
# The following line sets the timer to call the play function
# the first time only. 
screen.ontimer(play, 5)

def turnLeft():
	ship.setheading(ship.heading()+7)

# This tells the turtle graphics when a 4 is pressed to
# call the turnLeft function
screen.onkeypress(turnLeft,"4")

def forward():
	ship.fireEngine()

# This tells the turtle graphics when a 5 is pressed to 
# call the forward function when immediately calls the 
# fireEngine function on the ship.
screen.onkeypress(forward,"5")


