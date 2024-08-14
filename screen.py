from pygame import display

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 160
SCALE = 3

def get_screen():
    return display.set_mode((SCREEN_WIDTH * SCALE, SCREEN_HEIGHT * SCALE))