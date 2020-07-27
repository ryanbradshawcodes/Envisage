# Envisage - Ryan Bradshaw

TITLE = "Envisage"
WIDTH = 1920
HEIGHT = 1080
FPS = 60
FONT_NAME = "arial"
HS_File = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
MY_SPRITESHEET = "my_spritesheet.png"

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (53, 81, 210)
LIGHTERBLUE = (102, 178, 255)

# Game settings
CHAR_JUMP = 30
CHAR_ACC = 0.9
CHAR_FRIC = -0.15
CHAR_GRAV = 0.6
QUESTION_FREQ = 15

# Starting platforms
PLATFORM_LIST = [(WIDTH / 2, HEIGHT - 500),
                 (WIDTH / 2 - 50, HEIGHT * 3/4),
                 (1800, HEIGHT - 350),
                 (1500, 200),
                 (500, 100),
                 (100, 700)]
