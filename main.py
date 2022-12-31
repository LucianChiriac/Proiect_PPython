import sys
import pygame
from globalSettings import *
from mapGenerator import *
from pygame.locals import *
from gameplay import *
pygame.init()


def main():
    fps = pygame.time.Clock()
    global trajectory
    displaysurface = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Game")
    bubble_grid = get_bubble_specs()
    paint_game_window()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                dest_pos = pygame.mouse.get_pos()
                angle = getAngle(SHOOTER, dest_pos)
                trajectory = bubbleTrajectory(SHOOTER, angle)
                for coords in trajectory:
                    paint_game_window()
                    paint_bubble(WINDOW, coords[0], coords[1], BLUE)
                    pygame.display.update()
                    fps.tick(60)


if __name__ == "__main__":
    main()
