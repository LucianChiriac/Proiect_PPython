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
    global LOST_GAME
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
        # check if game is lost
        if row == MAXROWS-1:
            LOST_GAME = True
            r = row+1
            c = col
        else:
            # check wether left-side or right side
            if trajectory[-1][0] < bubble_grid[row][col][0]:
                newX = bubble_grid[row+1][col-(1-d)][0]
                newY = bubble_grid[row+1][col-(1-d)][1]
                r = row+1
                c = col-(1-d)
                if col-(1-d) < 0:  # special case
                    newX = bubble_grid[row+1][0][0]
                    newY = bubble_grid[row+1][0][1]
                    c = 0
                trajectory[-1] = (newX, newY)

            else:
                newX = bubble_grid[row+1][col+d][0]
                newY = bubble_grid[row+1][col+d][1]
                r = row+1
                c = col+d
                if col+d >= COLS:
                    newX = bubble_grid[row+1][COLS-1][0]
                    newY = bubble_grid[row+1][COLS-1][1]
                    c = COLS-1
                trajectory[-1] = (newX, newY)

        # Step 2: check if point of impact is above middle right point of ball, so bubble will be placed on same row, next position, or analogue, left
    if trajectory[-1][1] <= bubble_grid[row][col][1]:
        if trajectory[-1][0] < bubble_grid[row][col][0]:
            newX = bubble_grid[row][col-1][0]
            newY = bubble_grid[row][col-1][1]
            trajectory[-1] = (newX, newY)
            r = row
            c = col-1
        else:
            newX = bubble_grid[row][col+1][0]
            newY = bubble_grid[row][col+1][1]
            trajectory[-1] = (newX, newY)
            r = row
            c = col+1
    # special case - last row
    # if row == 0:
    #     newX = bubble_grid[row][col][0]
    #     newY = bubble_grid[row][col][1]
    #     trajectory[-1] = (newX, newY)
    #     r = row
    #     c = col
    return trajectory, r, c, LOST_GAME


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
        for c in range(0, COLS):
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
        dmin = 99999
        col = 0
        print(pos[0], pos[1])
        for c in range(COLS):
            d = dist([pos[0], pos[1]], [bubble_grid[0]
                     [c][0], bubble_grid[0][c][1]])
            if d < dmin:
                if not bubble_grid[0][c][3]:
                    print(bubble_grid[0][c][0], bubble_grid[0][c][1], d, c)
                    dmin = d
                    col = c
        return True, 0, col
    return False, None, None


# function to add the Shot bubble to the matrix
def add_bubble(pos, color, r, c):
    global LOST_GAME
    bubble_grid[r][c] = [pos[0], pos[1], color, True]
    if r == MAXROWS:
        LOST_GAME = True
    return LOST_GAME


def get_neighbours(row, col):
    neighbours = []
    d = row % 2
    if row-1 >= 0:
        if col-(1-d) >= 0:
            neighbours.append((row-1, col-(1-d)))
        if col+d < MAXCOLS:
            neighbours.append((row-1, col+d))
    if col-1 >= 0:
        neighbours.append((row, col-1))
    if col+1 < MAXCOLS:
        neighbours.append((row, col+1))
    if row+1 < MAXROWS:
        if col+d < MAXCOLS:
            neighbours.append((row+1, col+d))
        if col-(1-d) >= 0:
            neighbours.append((row+1, col-(1-d)))
    return neighbours


def color_bubble_popper(row, col):
    global SCORE
    bubbles = []  # the list of bubbles that will be popped
    start = 0  # index
    bubbles.append((row, col))  # starts with the bubble just added
    while start < len(bubbles):
        x = bubbles[start][0]
        y = bubbles[start][1]
        neighbours = get_neighbours(x, y)
        for n in neighbours:  # check if there is a ball there, and if it's the same color
            if bubble_grid[n[0]][n[1]][3] and bubble_grid[n[0]][n[1]][2] == bubble_grid[x][y][2]:
                # check n is not already in bubbles
                if (n[0], n[1]) not in bubbles:
                    bubbles.append((n[0], n[1]))
        start += 1
    if len(bubbles) >= 3:  # condition to pop
        for b in bubbles:
            bubble_grid[b[0]][b[1]][3] = False
    # compute a score
    popped = len(bubbles)
    if popped < 3:
        SCORE += 0
    else:
        SCORE += int(5+1.7**popped)
    return bubble_grid, SCORE


def free_bubble_popper():
    global SCORE
    # goes over the entire bubble grid, sets bubbles that have no upper/lateral neighbours to False
    lista = []
    start = 0
    for c in range(COLS):
        if bubble_grid[0][c][3]:
            lista.append((0, c))
    while start < len(lista):
        neighbours = get_neighbours(lista[start][0], lista[start][1])
        for n in neighbours:
            if bubble_grid[n[0]][n[1]][3] and ((n[0], n[1]) not in lista):
                lista.append((n[0], n[1]))
        start += 1

    # now go through entire bubble grid; bubbles that are not in "lista" are freestanding and need to be popped
    popped = 0
    for i in range(MAXROWS):
        for j in range(COLS):
            if (i, j) not in lista and (bubble_grid[i][j][3]):
                bubble_grid[i][j][3] = False
                popped += 1
    # compute a score)
    if popped > 0:
        SCORE += int(2+1.2**popped)
    return bubble_grid, SCORE

# check if game is won


def check_won_game():
    count = 0
    for r in range(MAXROWS):
        for c in range(COLS):
            if bubble_grid[r][c][3]:
                count += 1
    if count == 0:
        return True
    return False

# reset variables once game over


def reset():
    global SCORE
    global bubble_grid
    global LOST_GAME
    global WON_GAME
    global trajectory

    SCORE = 0
    bubble_grid.clear()
    LOST_GAME = False
    WON_GAME = False
    trajectory.clear()
