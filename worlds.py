import pygame
import enum
import assets
import os
import json

from constants import TileType


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


# Paths will need to be based on some OS base path or something
# https://stackoverflow.com/questions/56639952/what-does-pathlib-path-cwd-return

def get_offline_map_list():
    offline_maps = []

    for root, dirs, files in os.walk("./save/maps/"):

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
            #map_meta.set_thumb(pygame.image.load('./save/maps/default_thumb.png').convert_alpha())
            map_meta.set_thumb(pygame.image.load('./save/maps/default_thumb.png'))
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

    with open(map_meta.path + "/map.txt") as map_data:
        lines = [line.strip('\n') for line in map_data.readlines()]

        map_tiles = [[None] * map_meta.size[0]] * map_meta.size[1]
        map_spritegroup = pygame.sprite.Group()
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
                if char not in valid_chars:
                    return "Map contains invalid tiles!"

                tile_type = TileType(char)

                if tile_type == TileType.PATH:
                    paths.append((row, col))
                elif tile_type == TileType.START:
                    if start is None:
                        start = (row, col)
                    else:
                        return "There are too many start tiles in the map!"
                elif tile_type == TileType.KING:
                    if king is None:
                        king = (row, col)
                    else:
                        return "There are too many king tiles in the map!"

                new_tile = Tile(tile_type, (row, col))
                map_tiles[row][col] = new_tile
                map_spritegroup.add(new_tile)



    map = Map(map_meta, map_tiles, map_spritegroup, paths, start, king)
    return map


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, grid_loc):
        super().__init__()

        self.tile_type = tile_type
        self.image = assets.get_tile_asset(tile_type)
        self.rect = self.image.get_rect()
        self.grid_loc = grid_loc

    def update_screen_position(self, position):
        self.rect.center = position


class Map:
    def __init__(self, map_meta, tiles, spritegroup, path_locs, start_loc, king_loc):

        self.map_meta = map_meta
        self.tiles = tiles
        self.spritegroup = spritegroup

        self.path_locs = path_locs

    def update_tile_screen_positions(self, viewport_topleft, zoom):
        # Set rect center for every tile according to the current map position/zoom
        pass

    def render(self):
        pass


print(load_map(get_offline_map_list()[0]).tiles)
