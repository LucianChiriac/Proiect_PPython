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
    SHOOTER_COLOR = random.sample(COLORS, 1)[0]
    LOADED_COLOR = SHOOTER_COLOR
    NEXT_COLOR = random.sample(COLORS, 1)[0]
    displaysurface = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Game")
    bubble_grid = get_bubble_specs()
    paint_game_window(LOADED_COLOR, NEXT_COLOR)
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
                trajectory, r, c = bubbleTrajectory(SHOOTER, angle)
                for coords in trajectory:
                    paint_game_window(LOADED_COLOR, NEXT_COLOR)
                    paint_bubble(WINDOW, coords[0], coords[1], SHOOTER_COLOR)
                    pygame.display.update()
                    fps.tick(60)
                add_bubble(trajectory[-1], SHOOTER_COLOR, r, c)
                bubble_grid = color_bubble_popper(r, c)
                paint_game_window(LOADED_COLOR, NEXT_COLOR)
                pygame.display.update()
                fps.tick(60)
                SHOOTER_COLOR = LOADED_COLOR


if __name__ == "__main__":
    main()
