import pygame as pg
pg.font.init()


# Colors to be used in app (RGB format)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 102, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (153, 0, 153)
GRAY = (128, 128, 128)
BCKG_UP = (153, 214, 255)
BCKG_DOWN = (255, 179, 179)
COLORS = [RED, GREEN, BLUE, ORANGE, PURPLE]  # colors used for bubbles


# Fonts
Score_font = pg.font.SysFont("Times New Roman", 40)
End_game_font = pg.font.SysFont("Times new Roman", 75)
Font = pg.font.SysFont("Times New Roman", 30)

# Bubble specs
VELOCITY = 15  # speed with which bubble flies
RADIUS = 25
# Bubble matrix size
ROWS = 15
COLS = 15
LIMIT = 20  # if matrix reaches this size, it's game over
bubble_coords = []  # matrix of bubble "centers"

# Screen specs
SCREEN_SIZE = (800, 700)  # WIDTH, HEIGHT
UPPER_MENU_HEIGHT = 50  # bar for score and other info
LOWER_MENU_HEIGHT = 75  # bar for ball to be shot, and next balls
WINDOW = pg.display.set_mode(SCREEN_SIZE)  # the actual game screen
pg.display.set_caption("Bubbles!")  # Caption to appear on window
# position of the bubble to be launched (bottom screen)
SHOOTER = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]-LOWER_MENU_HEIGHT/2)

SCORE = 0
