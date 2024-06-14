import pygame
pygame.init()

import worlds
from classes import *

from classes import GridCoordinate


def drive_surrounding_gc():
    new_gc = GridCoordinate(5, 5)
    return new_gc.get_surrounding()

def drive_get_gridcoordinate():
    pygame.display.set_mode((1920, 1080))
    map_meta = worlds.get_offline_map_list()[0]
    loaded_map = worlds.load_map(map_meta) # Won't work without reference to game class
    return loaded_map.get_gridcoordinate(Point(800, 800))


def main():
    print(drive_get_gridcoordinate())


if __name__ == "__main__":
    main()
