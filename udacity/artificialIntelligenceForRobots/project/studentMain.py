# ----------
# Background
# 
# A robotics company named Trax has created a line of small self-driving robots 
# designed to autonomously traverse desert environments in search of undiscovered
# water deposits.
#
# A Traxbot looks like a small tank. Each one is about half a meter long and drives
# on two continuous metal tracks. In order to maneuver itself, a Traxbot can do one
# of two things: it can drive in a straight line or it can turn. So to make a 
# right turn, A Traxbot will drive forward, stop, turn 90 degrees, then continue
# driving straight.
#
# This series of questions involves the recovery of a rogue Traxbot. This bot has 
# gotten lost somewhere in the desert and is now stuck driving in an almost-circle: it has
# been repeatedly driving forward by some step size, stopping, turning a certain 
# amount, and repeating this process... Luckily, the Traxbot is still sending all
# of its sensor data back to headquarters.
#
# In this project, we will start with a simple version of this problem and 
# gradually add complexity. By the end, you will have a fully articulated
# plan for recovering the lost Traxbot.
# 
# ----------
# Part One
#
# Let's start by thinking about circular motion (well, really it's polygon motion
# that is close to circular motion). Assume that Traxbot lives on 
# an (x, y) coordinate plane and (for now) is sending you PERFECTLY ACCURATE sensor 
# measurements. 
#
# With a few measurements you should be able to figure out the step size and the 
# turning angle that Traxbot is moving with.
# With these two pieces of information, you should be able to 
# write a function that can predict Traxbot's next location.
#
# You can use the robot class that is already written to make your life easier. 
# You should re-familiarize yourself with this class, since some of the details
# have changed. 
#
# ----------
# YOUR JOB
#
# Complete the estimate_next_pos function. You will probably want to use
# the OTHER variable to keep track of information about the runaway robot.
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *
from math import *
from matrix import *
import random


# This is the function you have to write. The argument 'measurement' is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.

    if not OTHER: # this is the first measurement
        OTHER = [[],[],[]]

    OTHER[0].append(measurement)
    #print(OTHER[0][0][0])
    initial_x = OTHER[0][0][0]
    initial_y = OTHER[0][0][1]        
    

    dt = 0.8
    
    x = matrix([[initial_x], [initial_y], [0.], [0.]]) # initial state (location and velocity)

    u = matrix([[0.], [0.], [0.], [0.]]) # external motion
    
    #### DO NOT MODIFY ANYTHING ABOVE HERE ####
    #### fill this in, remember to use the matrix() function!: ####
    
    prob = 0.01
    measurment_uncertainty = 0.001    
    
    
    P =  matrix([[0.,0.,0.,0.],[0.,0.,0.,0.],[0.,0.,prob,0.],[0.,0.,0.,prob]])# initial uncertainty: 0 for positions x and y, 1000 for the two velocities (diagonal matrix first two diagonals for uncertainty of x,y position, next two for uncertainity of x,v velocites)
    F =  matrix([[1.,0.,dt,0.],[0.,1.,0.,dt],[0.,0.,1.,0.],[0.,0.,0.,1.]])# next state function: generalize the 2d version to 4d
    H =  matrix([[1,0,0,0],[0,1,0,0]])# measurement function: reflect the fact that we observe x and y but not the two velocities - projection matrix projecting position and not velocity
    R =  matrix([[measurment_uncertainty,0.],[0.,measurment_uncertainty]])# measurement uncertainty: use 2x2 matrix with 0.1 as main diagonal
    I =  matrix([[1.,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])# 4d identity matrix



    def filter(x, P, measurements):
        for n in range(len(measurements)):
            
            # prediction
            x = (F * x) + u
            P = F * P * F.transpose()
            
            
            # measurement update
            Z = matrix([measurements[n]])
            y = Z.transpose() - (H * x)
            S = H * P * H.transpose() + R
            K = P * H.transpose() * S.inverse()
            x = x + (K * y)
            P = (I - (K * H)) * P
     
        x = (F * x) + u
        P = F * P * F.transpose()
        
        return x, P

    measurements = OTHER[0]
    newX, newP = filter(x,P,measurements)

    xy_estimate = (newX.value[0][0],newX.value[1][0])
    OTHER[1] = newX
    OTHER[2] = newP
    
    print('meas: ', measurement, ' estimate: ', xy_estimate)    
    
    
    return xy_estimate, OTHER 

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want.

### Original demo_grading function
 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 10: 
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        print('error',error)
        if error <= distance_tolerance:
            print ("You got it right! It took you ", ctr, " steps to localize.")
            localized = True
        if ctr == 10:
            print ("Sorry, it took you too many steps to localize the target.")
    return localized


### Visualiing demo_grading function

def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    #For Visualization
    import turtle    #You need to run this locally to use the turtle module
    window = turtle.Screen()
    window.bgcolor('white')
    size_multiplier= 25.0  #change Size of animation
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.5, 0.5, 0.5)
    measured_broken_robot = turtle.Turtle()
    measured_broken_robot.shape('circle')
    measured_broken_robot.color('red')
    measured_broken_robot.resizemode('user')
    measured_broken_robot.shapesize(0.5, 0.5, 0.5)
    prediction = turtle.Turtle()
    prediction.shape('arrow')
    prediction.color('blue')
    prediction.resizemode('user')
    prediction.shapesize(0.5, 0.5, 0.5)
    prediction.penup()
    broken_robot.penup()
    measured_broken_robot.penup()
    #End of Visualization
    while not localized and ctr <= 10:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        print(error)
        if error <= distance_tolerance:
            print ("You got it right! It took you ", ctr, " steps to localize.")
            localized = True
        if ctr == 10:
            print ("Sorry, it took you too many steps to localize the target.")
        #More Visualization
        measured_broken_robot.setheading(target_bot.heading*180/pi)
        measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
        measured_broken_robot.stamp()
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
        broken_robot.stamp()
        prediction.setheading(target_bot.heading*180/pi)
        prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
        prediction.stamp()
        #End of Visualization
    turtle.done()
    return localized



# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER
    
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
test_target.set_noise(0.0, 0.0, 0.0)

demo_grading(estimate_next_pos, test_target)