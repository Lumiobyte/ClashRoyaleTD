import enum
import os
import pygame

ROOT_DIR = os.path.split(os.path.abspath(__file__))[0]  # Path to the root folder of the game files
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets/')
DATA_DIR = os.path.join(ROOT_DIR, 'save/')

WIDTH = 1920
HEIGHT = 1080
FPS = 60

H_CENTER = 960
V_CENTER = 540


class Colours:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    LIGHT_YELLOW = (247, 240, 141)
    LIGHT_GREEN = (182, 245, 140)
    DARK_GREEN = (62, 108, 40)
    LIGHT_GRAY = (135, 135, 135)
    LIGHT_BROWN = (217, 192, 104)

    # UI Colours
    PANEL_DARKGREY = (33, 33, 33)
    INFOBOX_GREY = (41, 41, 41)
    INFOBOX_BORDER = (119, 161, 154)
    BUTTON = (220, 242, 239)
    BUTTON_HOVER = (119, 161, 154)
    TEXT_SUBTITLE = (191, 191, 191)
    TEXT_LIGHT = (223, 235, 234)
    TEXT_DARK = ()


class TextSize:
    TINY = pygame.font.Font("./assets/fonts/segoe/segoe-ui.ttf", 16)
    SMALL = pygame.font.Font("./assets/fonts/segoe/segoe-ui.ttf", 24)
    SMALL_BOLD = pygame.font.Font("./assets/fonts/segoe/segoe-ui-bold.ttf", 24)
    MEDIUM = pygame.font.Font("./assets/fonts/segoe/segoe-ui.ttf", 32)
    LARGE = pygame.font.Font("./assets/fonts/segoe/segoe-ui.ttf", 32)
    MED_BOLD = pygame.font.Font("./assets/fonts/segoe/segoe-ui-bold.ttf", 48)
    LARGE_BOLD = pygame.font.Font("./assets/fonts/segoe/segoe-ui-bold.ttf", 64)


class TileType(enum.Enum):
    NULL = '.'
    START = 'S'
    PATH = '#'
    PLACEABLE = 'P'
    KING = 'K'
