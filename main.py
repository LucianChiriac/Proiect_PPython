import sys
import pygame
from globalSettings import *
import globalSettings
from mapGenerator import *
from pygame.locals import *
from gameplay import *
import random
import json
import datetime
import os
pygame.init()


def main():

    # check json file exists
    if not os.path.isfile('history.json'):
        with open('history.json', 'w') as jsonFile:
            jsonFile.write(json.dumps({}))
    with open('history.json', 'r') as jsonFile:
        jsonData = json.load(jsonFile)
        jsonData = json.dumps(jsonData)
        jsonData = json.loads(jsonData)

    fps = pygame.time.Clock()
    global trajectory
    global SCORE
    global LOST_GAME
    global WON_GAME
    global COLORS, COLORS_1, COLORS_2
    global LEVEL
    global MAXROWS
    if LEVEL == 1:
        COLORS = COLORS_1
        rows = MAXROWS - 5
    else:
        COLORS = COLORS_2
        rows = MAXROWS - 3
    SHOOTER_COLOR = random.sample(COLORS, 1)[0]
    LOADED_COLOR = SHOOTER_COLOR
    NEXT_COLOR = random.sample(COLORS, 1)[0]
    displaysurface = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Game")
    bubble_grid = get_bubble_specs(COLORS, rows)
    paint_game_window(LOADED_COLOR, NEXT_COLOR, SCORE,
                      LOST_GAME, WON_GAME, LEVEL)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                timestamp = datetime.datetime.now()
                timestamp = str(timestamp)
                jsonData[timestamp] = "quit"
                with open('history.json', 'w') as jsonFile:
                    json.dump(jsonData, jsonFile)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                LOADED_COLOR = NEXT_COLOR
                NEXT_COLOR = random.sample(COLORS, 1)[0]
                dest_pos = pygame.mouse.get_pos()
                angle = getAngle(SHOOTER, dest_pos)
                trajectory, r, c, LOST_GAME = bubbleTrajectory(SHOOTER, angle)
                for coords in trajectory:
                    paint_game_window(
                        LOADED_COLOR, NEXT_COLOR, SCORE, LOST_GAME, WON_GAME, LEVEL)
                    paint_bubble(WINDOW, coords[0], coords[1], SHOOTER_COLOR)
                    pygame.display.update()
                    fps.tick(60)
                if not LOST_GAME:
                    add_bubble(trajectory[-1], SHOOTER_COLOR, r, c)
                    bubble_grid, SCORE = color_bubble_popper(r, c)
                    bubble_grid, SCORE = free_bubble_popper()
                paint_game_window(LOADED_COLOR, NEXT_COLOR,
                                  SCORE, LOST_GAME, WON_GAME, LEVEL)
                WON_GAME = check_won_game()
                if WON_GAME and LEVEL == 1:
                    timestamp = datetime.datetime.now()
                    timestamp = str(timestamp)
                    jsonData[timestamp] = "passed level 1"
                    with open('history.json', 'w') as jsonFile:
                        json.dump(jsonData, jsonFile)
                    reset()
                    pygame.event.clear()
                    LEVEL = 2
                    main()
                elif LOST_GAME or WON_GAME:
                    if LOST_GAME:
                        timestamp = datetime.datetime.now()
                        timestamp = str(timestamp)
                        jsonData[timestamp] = "LOST GAME"
                        with open('history.json', 'w') as jsonFile:
                            json.dump(jsonData, jsonFile)
                    if WON_GAME:
                        timestamp = datetime.datetime.now()
                        timestamp = str(timestamp)
                        jsonData[timestamp] = "WON GAME!"
                        with open('history.json', 'w') as jsonFile:
                            json.dump(jsonData, jsonFile)
                    reset()
                    pygame.event.clear()
                    LEVEL = 1
                    main()
                pygame.display.update()
                fps.tick(60)
                SHOOTER_COLOR = LOADED_COLOR


if __name__ == "__main__":
    main()

# la final de joc, fisier JSON updatat la fiecare cu Dictionar (timestamp : status (lost/won/exit)
# json.load()
# json.dump()
