import pygame
import enum
import assets
import os
import json

from constants import *
from classes import *


# Notes
# Gridcoordinate class would be useful - support methods like getabove, getbelow, check surrounds etc
# Enums or constants for possible zoom levels e.g. 2, 1, 0.8, etc
# Culling so that tiles where top left is outside the viewport area are not rendered at all.

class MapMeta:
    def __init__(self, name, author, size, path, editable):
        self.thumb = None
        self.name = name
        self.author = author
        self.size = size
        self.path = path
        self.editable = editable

    def set_thumb(self, new_thumb):
        self.thumb = new_thumb


# TODO: Paths will need to be based on some OS base path or something
# https://stackoverflow.com/questions/56639952/what-does-pathlib-path-cwd-return

def get_offline_map_list():
    offline_maps = []

    for root, dirs, files in os.walk(DATA_DIR+"maps/"):

        if len(files) < 1:
            continue
        if 'metadata.json' not in files or 'map.txt' not in files:
            continue

        with open(root + "/metadata.json") as metadata_json:
            data = json.load(metadata_json)

            if "invalid" in data:
                continue

            try:
                map_meta = MapMeta(
                    data['name'],
                    data['author'],
                    data['size'],
                    root,
                    False if data.get("origin") == "online" else True
                )
            except KeyError:
                continue

        if 'thumb.png' not in files:
            map_meta.set_thumb(pygame.image.load(DATA_DIR+'/maps/default_thumb.png').convert_alpha())
        else:
            map_meta.set_thumb(pygame.image.load(root + '/thumb.png').convert_alpha())

        offline_maps.append(map_meta)

    return offline_maps


def load_map(map_meta):
    """
    Load map from file. Returns descriptive error string if loading failed.
    :param map_meta: MapMeta object of the map to load
    :return: Map
    """

    # TODO: Need to ensure that there are no dead ends on the map. Only two ends are start and king
    # Easiest way is to just disallow any path tile from having more than two adjacent path tiles. Prevents branches

    with open(map_meta.path + "/map.txt") as map_data:
        lines = [line.strip('\n') for line in map_data.readlines()]

        # Beware [[v]*n]*n
        # map_tiles = [[None] * map_meta.size[0] for i in range(map_meta.size[1])] # Access is [y][x]
        map_tiles = [[None] * map_meta.size[1] for i in range(map_meta.size[0])]  # Access is [x][y]
        paths = []
        start = None
        king = None

        valid_chars = ['.', '#', 'S', 'P', 'K']

        if not len(lines) == map_meta.size[1]:
            return "Map is formatted incorrectly!"

        for row, line in enumerate(lines):
            if not len(line) == map_meta.size[0]:
                return "Map is formatted incorrectly!"

            for col, char in enumerate(line):

                tile_pos = (col, row)  # x, y

                if char not in valid_chars:
                    return "Map contains invalid tiles!"

                tile_type = TileType(char)

                if tile_type == TileType.PATH:
                    paths.append(tile_pos)
                elif tile_type == TileType.START:
                    if start is None:
                        start = tile_pos
                    else:
                        return "There are too many start tiles in the map!"
                elif tile_type == TileType.KING:
                    if king is None:
                        king = tile_pos
                    else:
                        return "There are too many king tiles in the map!"

                new_tile = Tile(tile_type, tile_pos)
                map_tiles[col][row] = new_tile

    final_map = Map(map_meta, map_tiles, paths, start, king)
    return final_map


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, grid_loc):
        super().__init__()

        self.tile_type = tile_type
        self.image = assets.get_tile_asset(tile_type)
        self.rect = self.image.get_rect()
        self.grid_loc = grid_loc

    def update_pos(self, viewport_pos):
        tile_pos = (
            viewport_pos.x + self.rect.width * self.grid_loc[0],
            viewport_pos.y + self.rect.height * self.grid_loc[1]
        )

        self.rect = self.rect.move_to(topleft=tile_pos)

    def update_zoom(self, factor):
        # Zoom is not implemented currently
        # pygame.transform.scale(self.image, self.rect)
        pass


class Map:
    def __init__(self, map_meta, tiles, path_locs, start_loc, king_loc):

        self.map_meta = map_meta
        self.tiles = tiles

        self.spritegroup = pygame.sprite.Group()
        for row in self.tiles:
            for tile in row:
                self.spritegroup.add(tile)

        self.path_locs = path_locs
        self.start_loc = start_loc
        self.king_loc = king_loc

        # Allow default viewport loc & zoom to be passed
        self.viewport_topleft = Point(0, 0)
        self.zoom = 1

        self.pan_viewport(self.viewport_topleft)
        self.zoom_viewport(self.zoom)

        self.viewport_area = pygame.Rect(0, 0, WIDTH - 500, HEIGHT)

    def pan_viewport(self, new_pos):
        self.viewport_topleft = new_pos

        for row in self.tiles:
            for tile in row:
                tile.update_pos(self.viewport_topleft)

    def zoom_viewport(self, new_zoom):
        self.zoom = new_zoom
        for row in self.tiles:
            for tile in row:
                tile.update_zoom(self.zoom)

    def update(self):
        pass

    def render(self, surface):
        self.spritegroup.draw(surface)
