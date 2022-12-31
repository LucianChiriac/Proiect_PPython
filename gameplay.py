# This file controls the gameplay
# throwing the ball
# bouncing the ball on walls
# calculating collisions (balls to be popped)


from math import atan2, degrees, cos, sin, radians, dist
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
    # global trajectory
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
        final, row, col = finalCollision(trajectory[-1], angl)
    if row % 2 == 0:
        d = 0
    else:
        d = 1
    # knowing the point of impact, calculate where will the bubble be snapped in place
        # Step 1: check if the point of impact is below the half of the ball, which means ball will be placed on next row
    if trajectory[-1][1] > bubble_grid[row][col][1]:
        # check wether left-side or right side
        if trajectory[-1][0] < bubble_grid[row][col][0]:
            newX = bubble_grid[row+1][col-(1-d)][0]
            newY = bubble_grid[row+1][col-(1-d)][1]
            trajectory[-1] = (newX, newY)
            r = row+1
            c = col-(1-d)
            print("Lower Left", d, r, c)
        else:
            newX = bubble_grid[row+1][col+d][0]
            newY = bubble_grid[row+1][col+d][1]
            trajectory[-1] = (newX, newY)
            r = row+1
            c = col+d
            print("Lower Right", d, r, c)
        # Step 2: check if point of impact is above middle right point of ball, so bubble will be placed on same row, next position, or analogue, left
    if trajectory[-1][1] <= bubble_grid[row][col][1]:
        if trajectory[-1][0] < bubble_grid[row][col][0]:
            newX = bubble_grid[row][col-1][0]
            newY = bubble_grid[row][col-1][1]
            trajectory[-1] = (newX, newY)
            r = row
            c = col-1
            print("Left", d, r, c)
        else:
            newX = bubble_grid[row][col+1][0]
            newY = bubble_grid[row][col+1][1]
            trajectory[-1] = (newX, newY)
            r = row
            c = col+1
            print("Right", d, r, c)
    return trajectory, r, c


# a function to check for collisions between bubbles and lateral walls
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
    # check all bubble, starting from lower rows upwards
    for r in reversed(range(0, MAXROWS)):
        for c in range(0, MAXCOLS):
            # check if there is a ball in that particular position
            if bubble_grid[r][c][3]:  # filled=True
                # check if the two bubbles are at a distance smaller or equal than 2*Radius (means they are adjacent)
                distanta = dist([pos[0], pos[1]], [
                                bubble_grid[r][c][0], bubble_grid[r][c][1]])
                if distanta <= 2 * RADIUS:
                    # also need to return the position of impact, to see where to snap the bubble in place
                    return True, r, c
    # the bubble reached the upper bound of the screen without meeting other bubbles
    if pos[1] < RADIUS+UPPER_MENU_HEIGHT+UPAD:
        return True
    return False, None, None


# function to add the Shot bubble to the matrix
def add_bubble(pos, color, r, c):
    bubble_grid[r][c] = (pos[0], pos[1], color, True)
    # A function to pop the bubbles and update the matrix


def bubble_pop(start_pos):
    x = 2
