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
CURRENT_COLOR = None
NEXT_COLOR = None

# Fonts
Score_font = pg.font.SysFont("Times New Roman", 40)
End_game_font = pg.font.SysFont("Times new Roman", 75)
Font = pg.font.SysFont("Times New Roman", 30)


# Screen specs
SCREEN_SIZE = (600, 700)  # WIDTH, HEIGHT
UPPER_MENU_HEIGHT = 50  # bar for score and other info
LOWER_MENU_HEIGHT = 75  # bar for ball to be shot, and next balls
WINDOW = pg.display.set_mode(SCREEN_SIZE)  # the actual game screen
pg.display.set_caption("Bubbles!")  # Caption to appear on window
# position of the bubble to be launched (bottom screen)
SHOOTER = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]-LOWER_MENU_HEIGHT/2)
SCORE = 0
# padding between screen margins and actual objects
LPAD = 0
RPAD = 0
UPAD = 15
DPAD = 0

# Bubble specs
VELOCITY = 10  # speed with which bubble flies
RADIUS = 25

# Bubble matrix size
MAXROWS = (SCREEN_SIZE[1]-UPAD-DPAD-LOWER_MENU_HEIGHT -
           UPPER_MENU_HEIGHT)//(2*RADIUS)
ROWS = MAXROWS - 5
MAXCOLS = (SCREEN_SIZE[0]-LPAD-RPAD)//(2*RADIUS)
COLS = MAXCOLS - 1

# Share the difference between the 2 paddings
DIFF = SCREEN_SIZE[0] - (COLS)*2*RADIUS
LPAD += DIFF//2
RPAD += DIFF//2
# LIMIT = 20  # if matrix reaches this size, it's game over
bubble_grid = []  # matrix of bubble wall, containing all info

trajectory = []
