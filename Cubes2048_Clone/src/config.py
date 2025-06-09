# Configuration and constants for Cubes 2048 clone
import os
import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BG_COLOR = (10, 20, 40)
GRID_COLOR = (30, 50, 80)
TEXT_COLOR = (255, 255, 255)

# Snake settings
SNAKE_SPEED = 200.0  # pixels per second
BOOST_MULTIPLIER = 1.8
SEGMENT_DISTANCE = 40

# Cube values and colors (matching 2048 style)
CUBE_COLORS = {
    2: (255, 90, 90),
    4: (90, 90, 255),
    8: (90, 255, 90),
    16: (255, 180, 120),
    32: (255, 140, 50),
    64: (255, 215, 0),
    128: (190, 255, 0),
    256: (140, 255, 220),
    512: (140, 180, 255),
    1024: (255, 140, 200),
    2048: (255, 255, 255),
}

FONT_NAME = None  # default pygame font

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')
IMAGE_DIR = os.path.join(ASSET_DIR, 'images')
SOUND_DIR = os.path.join(ASSET_DIR, 'sounds')
