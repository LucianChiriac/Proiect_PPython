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


def get_bubble_coordinates():
    for r in range(ROWS):
        coords = []  # one row of bubble "centers"
        for c in range(COLS):
            x = c*r*2+RADIUS
            y = MENU_HEIGHT + r*2*RADIUS+r
            coords.append((x, y))
        bubble_coords.append(coords)


def paint_bubbleWall():
    # pygame.Rect(left,top,width,height)
    for r in range(ROWS):
        for c in range(COLS):
            color = random.sample(COLORS, 1)[0]  # set color at random
            center = bubble_coords[r][c]
            pg.draw.circle(WINDOW, color, center, RADIUS, width=2)


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
    paint_lower_menu()
    pg.display.update()
