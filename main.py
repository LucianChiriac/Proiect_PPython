import sys
import pygame
from globalSettings import *
from mapGenerator import *
from pygame.locals import *
pygame.init()


def main():
    fps = pygame.time.Clock()
    displaysurface = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Game")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        paint_game_window()

        pygame.display.update()
        fps.tick(60)


if __name__ == "__main__":
    main()
