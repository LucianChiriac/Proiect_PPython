# This file controls the gameplay
# throwing the ball
# bouncing the ball on walls
# calculating collisions (balls to be popped)


from math import atan2, degrees, cos, sin, radians
from globalSettings import *
import sys

# function to calculate the angle between launching point, and destination point
# https://gist.github.com/darzo27/d25161f13686633bd52162044b30b7db


def getAngle(p1, p2):
    xdiff = p2[0] - p1[0]
    ydiff = p2[1] - p1[1]
    return -degrees(atan2(ydiff, xdiff))


# a function to calculate iterative positions of a ball (steps)
# https://stackoverflow.com/questions/46697502/how-to-move-a-sprite-according-to-an-angle-in-pygame
def nextBallPos(start_pos, angle):
    #global trajectory
    new_x = start_pos[0] + (VELOCITY*cos(radians(angle)))
    new_y = start_pos[1] - (VELOCITY*sin(radians(angle)))
    trajectory.append((new_x, new_y))


# a function to compute the trajectory of a bubble until it stopps
# it will save a vector of positions, which will then be plotted on the game map
def bubbleTrajectory(start_pos, angle):
    angl = angle
    global trajectory
    trajectory = [start_pos]
    final = False
    while not final:
        nextBallPos(trajectory[-1], angl)
        angl = wallCollision(trajectory[-1], angl)
        final = finalCollision(trajectory[-1], angl)
    return trajectory

# a function to check for collisions between bubbles and walls


def wallCollision(pos, angle):
    # ball bounces on the right wall
    if pos[0] + RADIUS >= SCREEN_SIZE[0]:
        angle = 180 - angle
    # ball bounces on the left wall
    if pos[0] - RADIUS <= 0:
        angle = 180 - angle
    return angle


# checks if bubble reached the bubble wall (final state)
def finalCollision(pos, angle):
    if pos[1] < RADIUS+UPPER_MENU_HEIGHT+UPAD:
        return True
    return False
