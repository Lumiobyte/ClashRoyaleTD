import pygame
from constants import Colours, TileType


def get_tile_asset(tile_type):
    image = pygame.Surface((80, 80))

    if tile_type == TileType.START:
        image.fill(Colours.RED)
    elif tile_type == TileType.PATH:
        image.fill(Colours.LIGHT_YELLOW)
    elif tile_type == TileType.PLACEABLE:
        image.fill(Colours.LIGHT_GREEN)
    elif tile_type == TileType.KING:
        image.fill(Colours.BLUE)
    elif tile_type == TileType.NULL:
        image.fill(Colours.LIGHT_GRAY)

    return image
