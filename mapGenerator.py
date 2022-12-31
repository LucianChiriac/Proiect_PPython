"""
This file draws the actual game window, containing:
 - Bubble wall
 - Bubble to be shot
 - Menu bar (containing score and other info)
 - Background and other 
"""

import pygame as pg
from globalSettings import *
import random


def paint_upper_menu():
    # draw the upper menu rectangle
    rect = pg.draw.rect(
        WINDOW, BCKG_UP, (0, 0, SCREEN_SIZE[0], UPPER_MENU_HEIGHT))
    # create the text to show score
    score_text = Score_font.render(
        f'Score: {SCORE}', True, PURPLE)
    # stick the text onto screen (middle positioning)
    WINDOW.blit(score_text, ((rect.size[0]-score_text.get_width())/2, 0))


def paint_lower_menu():
    # draw the lower menu rectangle
    rect = pg.draw.rect(
        WINDOW, BCKG_DOWN, (0, SCREEN_SIZE[1]-LOWER_MENU_HEIGHT, SCREEN_SIZE[0], LOWER_MENU_HEIGHT))
    # Draw the middle ball to be shot
    paint_bubble(WINDOW, SHOOTER[0], SHOOTER[1], RED)
    # Insert text message with color of next ball
    text = Font.render("Next bubble: ", True, PURPLE)
    WINDOW.blit(text, (SHOOTER[0]+100, SCREEN_SIZE[1] -
                (LOWER_MENU_HEIGHT+Font.get_height())/2))
    # Draw the "next" ball, after the text
    paint_bubble(WINDOW, SHOOTER[0]+125+text.get_width(), SCREEN_SIZE[1] -
                 (LOWER_MENU_HEIGHT)/2, BLUE)

# function to compute the center for all possibile bubbles on the game map


def get_bubble_specs():  # matrix of tuples of shape (x,y,color, filled) where x,y are the center coordinates, filled=True/False indicating wether there is a bubble there or not
    for r in range(MAXROWS):
        coords = []  # one row of bubble "centers"
        for c in range(MAXCOLS):
            x = (c*2+1+r % 2)*RADIUS
            y = UPPER_MENU_HEIGHT + (r*2+1)*RADIUS - r*7
            color = random.sample(COLORS, 1)[0]  # set color at random
            if r < ROWS and c < COLS:
                filled = True
            else:
                filled = False
            coords.append((x, y, color, filled))
        bubble_grid.append(coords)


def paint_bubbleWall():
    # pygame.Rect(left,top,width,height)
    for r in range(MAXROWS):
        for c in range(MAXCOLS):
            if (bubble_grid[r][c][3]):
                x, y, color = bubble_grid[r][c][0], bubble_grid[r][c][1], bubble_grid[r][c][2]
                paint_bubble(WINDOW, LPAD//2+x, UPAD+y, color)


def paint_bubble(screen, x, y, color):
    # paints a bubble centered in (x,y) of color "color" on the "screen"
    pg.draw.circle(screen, color, (x, y), RADIUS)
    # draw the contour of the circle
    pg.draw.circle(screen, BLACK, (x, y), RADIUS, width=1)
    # pg.display.update(screen)
    # updates the screen where bubble was painted


def get_shooter_rect():  # the bubble to be shot
    rect = pg.Rect(SHOOTER[0]-RADIUS, SHOOTER[1]-2*RADIUS, RADIUS*2, RADIUS*2)
    return rect


def paint_game_window():
    WINDOW.fill(WHITE)
    paint_upper_menu()
    paint_bubbleWall()
    paint_lower_menu()
    pg.display.update()
