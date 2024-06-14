import pygame
import enum
import assets
import os
import json

import misc
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

    for root, dirs, files in os.walk(DATA_DIR + "maps/"):

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
            map_meta.set_thumb(pygame.image.load(DATA_DIR + '/maps/default_thumb.png').convert_alpha())
        else:
            map_meta.set_thumb(pygame.image.load(root + '/thumb.png').convert_alpha())

        offline_maps.append(map_meta)

    return offline_maps


def load_map(game, map_meta, editable=False):
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

        if not len(lines) == map_meta.size[1]:
            return "Map is formatted incorrectly!"

        for row, line in enumerate(lines):
            if not len(line) == map_meta.size[0]:
                return "Map is formatted incorrectly!"

            for col, char in enumerate(line):

                tile_pos = GridCoordinate(col, row)  # x, y
                tile_type = tile_types.get(char, None)

                if tile_type is None:
                    return "Map contains invalid tiles!"

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

                new_tile = Tile(game.assets.get_tile_asset(tile_type), tile_type, tile_pos)
                map_tiles[col][row] = new_tile

    if editable:
        return EditableMap(game, map_meta, map_tiles, paths, start, king)
    else:
        return Map(game, map_meta, map_tiles, paths, start, king)


class Tile(pygame.sprite.Sprite):
    def __init__(self, asset, tile_type, grid_loc):
        super().__init__()

        self.tile_type = tile_type
        self.image = asset
        self.rect = self.image.get_rect()
        self.grid_loc = grid_loc

    def update_grid_loc(self, change):
        self.grid_loc += change

    def update_pos(self, viewport_pos):
        tile_pos = (
            viewport_pos.x + self.rect.width * self.grid_loc.x,
            viewport_pos.y + self.rect.height * self.grid_loc.y
        )

        self.rect = self.rect.move_to(topleft=tile_pos)

    def update_zoom(self, factor):
        # Zoom is not implemented currently
        # pygame.transform.scale(self.image, self.rect)
        pass


class Map:
    def __init__(self, game, map_meta, tiles, path_locs, start_loc, king_loc):
        self.game = game

        self.map_meta = map_meta
        self.tiles = tiles

        self.spritegroup = pygame.sprite.Group()
        for col in self.tiles:
            for tile in col:
                self.spritegroup.add(tile)

        self.tile_size = Point(self.tiles[0][0].rect.width, self.tiles[0][0].rect.height)
        self.map_limit = GridCoordinate(len(self.tiles), len(self.tiles[0]))

        self.path_locs = path_locs
        self.start_loc = start_loc
        self.king_loc = king_loc

        # Allow default viewport loc & zoom to be passed
        self.viewport_topleft = Point(0, 0)
        self.zoom = 1

        # Initialise pan and zoom
        self.pan_viewport(self.viewport_topleft)
        self.zoom_viewport(self.zoom)

        self.viewport_area = pygame.Rect(0, 0, WIDTH - 370, HEIGHT)  # 370 is the width of the UI side panel

    def get_gridcoordinate(self, coordinate: Point):
        adjusted_coord = coordinate - self.viewport_topleft

        gc = GridCoordinate(misc.clamp(adjusted_coord.x // self.tile_size.x, 0, self.map_limit.x - 1),
                            misc.clamp(adjusted_coord.y // self.tile_size.y, 0, self.map_limit.y - 1))

        return gc

    def pan_viewport(self, new_pos):

        # TODO: Limit panning range, don't allow to scroll infinitely in a direction
        # Limit e.g. + or - 3 tiles in any direction.

        self.viewport_topleft = new_pos

        for row in self.tiles:
            for tile in row:
                tile.update_pos(self.viewport_topleft)

    def pan_viewport_by(self, pan_dist):
        self.pan_viewport(self.viewport_topleft + pan_dist)

    def zoom_viewport(self, new_zoom):
        self.zoom = new_zoom
        for row in self.tiles:
            for tile in row:
                tile.update_zoom(self.zoom)

    def update(self):
        pass

    def render(self, surface):
        self.spritegroup.draw(surface)

    def highlight_tile(self, surface, position):
        if isinstance(position, GridCoordinate):
            gc = position
        else:
            gc = self.get_gridcoordinate(position)

        highlight_rect = pygame.Rect((gc.x * self.tile_size.x) + self.viewport_topleft.x,
                                     (gc.y * self.tile_size.y) + self.viewport_topleft.y,
                                     self.tile_size.x, self.tile_size.y)

        pygame.draw.rect(surface, Colours.RED, highlight_rect)


class EditableMap(Map):
    def __init__(self, game, map_meta, tiles, path_locs, start_loc, king_loc):
        Map.__init__(self, game, map_meta, tiles, path_locs, start_loc, king_loc)

        self.grid_limit = self.map_limit + GridCoordinate(1, 1)

        # Used for tallying up the total mouse movement distance from the relative movement each frame in move_all
        self.movement_tally = Point(0, 0)
        self.grid_movement_tally = GridCoordinate(0, 0)

    def get_gridcoordinate(self, coordinate: Point):
        adjusted_coord = coordinate - self.viewport_topleft

        gc = GridCoordinate(misc.clamp(adjusted_coord.x // self.tile_size.x, 0, self.grid_limit.x - 1),
                            misc.clamp(adjusted_coord.y // self.tile_size.y, 0, self.grid_limit.y - 1))

        return gc

    def create_tile(self, tile_loc, tile_type):
        new_tile = Tile(self.game.assets.get_tile_asset(tile_type), tile_type, tile_loc)
        new_tile.update_pos(self.viewport_topleft)
        new_tile.update_zoom(self.zoom)
        self.spritegroup.add(new_tile)

        return new_tile

    def set_tile(self, tile_loc, tile_type):

        # Determine whether to expand grid
        if tile_loc.x >= self.map_limit.x:
            new_col = []
            for y in range(self.map_limit.y):
                new_col.append(self.create_tile(GridCoordinate(tile_loc.x, y), TileType.NULL))

            self.tiles.append(new_col)

            self.map_limit.x += 1
            self.grid_limit.x += 1

        if tile_loc.y >= self.map_limit.y:
            for x in range(self.map_limit.x):
                self.tiles[x].append(self.create_tile(GridCoordinate(x, tile_loc.y), TileType.NULL))

            self.map_limit.y += 1
            self.grid_limit.y += 1

        # Update the tile
        self.spritegroup.remove(self.tiles[tile_loc.x][tile_loc.y])

        self.tiles[tile_loc.x][tile_loc.y] = self.create_tile(tile_loc, tile_type)

    def reset_move_all(self):
        self.movement_tally = Point(0, 0)
        self.grid_movement_tally = GridCoordinate(0, 0)

    def update_all_gridcoordinates(self, change):
        for col in self.tiles:
            for tile in col:
                tile.update_grid_loc(change)
                tile.update_pos(self.viewport_topleft)

    def move_all(self, new_movement):
        self.movement_tally += new_movement

        # Update the lists so that the tiles are moved in the lists correctly
        # Update each tiles grid_loc

        # Right/Left
        if self.movement_tally.x >= self.tile_size.x:  # Move right
            self.movement_tally.x -= self.tile_size.x
            self.grid_movement_tally.x += 1

            self.update_all_gridcoordinates(GridCoordinate(1, 0))

            new_col = []
            for y in range(self.map_limit.y):
                new_col.append(self.create_tile(GridCoordinate(0, y), TileType.NULL))

            self.tiles.insert(0, new_col)

            self.map_limit.x += 1
            self.grid_limit.x += 1

        elif self.movement_tally.x <= -self.tile_size.x and self.grid_movement_tally.x > 0:  # Move left
            self.movement_tally.x += self.tile_size.x
            self.grid_movement_tally.x -= 1

            self.update_all_gridcoordinates(GridCoordinate(-1, 0))

            for tile in self.tiles[0]:
                self.spritegroup.remove(tile)
            self.tiles.pop(0)

            self.map_limit.x -= 1
            self.grid_limit.x -= 1

        # Down/Up
        if self.movement_tally.y >= self.tile_size.y:  # Move down
            self.movement_tally.y -= self.tile_size.y
            self.grid_movement_tally.y += 1

            self.update_all_gridcoordinates(GridCoordinate(0, 1))

            for x in range(self.map_limit.x):
                self.tiles[x].insert(0, self.create_tile(GridCoordinate(x, 0), TileType.NULL))

            self.map_limit.y += 1
            self.grid_limit.y += 1

        elif self.movement_tally.y <= -self.tile_size.y and self.grid_movement_tally.y > 0:  # Move up
            self.movement_tally.y += self.tile_size.y
            self.grid_movement_tally.y -= 1

            self.update_all_gridcoordinates(GridCoordinate(0, -1))

            for x in range(self.map_limit.x):
                self.spritegroup.remove(self.tiles[x][0])
                self.tiles[x].pop(0)

            self.map_limit.y -= 1
            self.grid_limit.y -= 1

    def render_grid(self, surface, colour):

        coordinate = Point(0, 0) + self.viewport_topleft
        tile_width = self.tile_size.x

        x_range = [self.viewport_area.left, coordinate.x + (self.tile_size.x * self.grid_limit.x)]
        if coordinate.x > x_range[0]:
            x_range[0] = coordinate.x

        y_range = [self.viewport_area.top, coordinate.y + (self.tile_size.y * self.grid_limit.y)]
        if coordinate.y > y_range[0]:
            y_range[0] = coordinate.y

        while coordinate.x <= x_range[1]:
            pygame.draw.line(surface, colour, (coordinate.x, y_range[0]), (coordinate.x, y_range[1]), 1)
            coordinate = coordinate + Point(tile_width, 0)

        tile_height = self.tile_size.y
        while coordinate.y <= y_range[1]:
            pygame.draw.line(surface, colour, (x_range[0], coordinate.y), (x_range[1], coordinate.y), 1)
            coordinate += Point(0, tile_height)
