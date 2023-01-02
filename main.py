import sys
import pygame
from globalSettings import *
from mapGenerator import *
from pygame.locals import *
from gameplay import *
import random
pygame.init()


def main():
    fps = pygame.time.Clock()
    global trajectory
    global SCORE
    global LOST_GAME
    global WON_GAME
    SHOOTER_COLOR = random.sample(COLORS, 1)[0]
    LOADED_COLOR = SHOOTER_COLOR
    NEXT_COLOR = random.sample(COLORS, 1)[0]
    displaysurface = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Game")
    bubble_grid = get_bubble_specs()
    paint_game_window(LOADED_COLOR, NEXT_COLOR, SCORE, LOST_GAME, WON_GAME)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
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
                        LOADED_COLOR, NEXT_COLOR, SCORE, LOST_GAME, WON_GAME)
                    paint_bubble(WINDOW, coords[0], coords[1], SHOOTER_COLOR)
                    pygame.display.update()
                    fps.tick(60)
                if not LOST_GAME:
                    add_bubble(trajectory[-1], SHOOTER_COLOR, r, c)
                    bubble_grid, SCORE = color_bubble_popper(r, c)
                    bubble_grid, SCORE = free_bubble_popper()
                paint_game_window(LOADED_COLOR, NEXT_COLOR,
                                  SCORE, LOST_GAME, WON_GAME)
                WON_GAME = check_won_game()
                if LOST_GAME or WON_GAME:
                    reset()
                    pygame.event.clear()
                    main()
                pygame.display.update()
                fps.tick(60)
                SHOOTER_COLOR = LOADED_COLOR


if __name__ == "__main__":
    main()
