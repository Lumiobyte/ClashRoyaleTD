import pygame
import glob
import os
from constants import *
from classes import Point


image_ext = ('.png', '.jpg')
sound_ext = ('.wav', '.ogg', '.mp3')


def first_time_setup():
    pass

    # If not exists save/maps, save/ongoing - create them .
    # Everything else will be bundled into the exe


class AssetManager:
    def __init__(self, path=ASSETS_DIR+"auto/"):
        self.path = path
        self.assets = {}

        for container in glob.glob(path + "*"):
            folder = container.split('\\')[-1].lower()
            self.assets[folder] = {}

            for filepath in glob.glob(container + "/*"):
                file = filepath.split('\\')[-1].lower()
                loaded_asset = None

                if file.startswith("anim_"):
                    loaded_asset = AnimatedImage(filepath)
                elif file.endswith(image_ext):
                    loaded_asset = Image(filepath)
                elif file.endswith(sound_ext):
                    loaded_asset = pygame.mixer.Sound(filepath)
                elif file.endswith('.txt'):
                    loaded_asset = self.load_string(filepath)

                if loaded_asset:
                    self.assets[folder][file[0:-4]] = loaded_asset
                    # TODO: define top level dict before adding assets to it or keyerror


    def load_string(self, filepath):
        with open(filepath, "r") as file:
            lines = [line.strip() for line in file.readlines()]

        return lines

    def get(self, asset):
        asset_list = asset.split('.')  # For example image.logo or sound.click

        if len(asset_list) == 1:
            return self.assets[asset_list[0]]
        elif len(asset_list) == 2:
            return self.assets[asset_list[0]][asset_list[1]]

    def get_tile_asset(self, tile_type):

        if tile_type == TileType.START:
            return self.assets['image']['start'].image
        elif tile_type == TileType.PATH:
            return self.assets['image']['path'].image
        elif tile_type == TileType.PLACEABLE:
            return self.assets['image']['placeable'].image
        elif tile_type == TileType.KING:
            return self.assets['image']['king'].image
        elif tile_type == TileType.NULL:
            return self.assets['image']['empty'].image



class Image:
    def __init__(self, filepath):

        self.image = pygame.image.load(filepath).convert_alpha()

        # Implement image scaling?
        # if(not self.scaling_factor == Point(1, 1)):
            # Use smoothscale if this gets too ugly
            # self.image = pygame.transform.scale(self.image, (Point(self.image.get_width(), self.image.get_height()) * self.scaling_factor).tuple())

    def get_rect(self):
        return self.image.get_rect()

    def render(self, screen, pos: Point, centered=False):
        render_pos = pos
        if centered:
            render_pos -= Point(self.image.get_width() / 2, self.image.get_height() / 2)
        screen.blit(self.image, render_pos.tuple())


class AnimatedImage:
    def __init__(self, image_directory, frame_length=None):

        self.frames = []
        for filepath in glob.glob(f"{image_directory}/*.png"):
            self.frames.append(Image(filepath))

        self.num_frames = len(self.frames)
        self.current_frame = 0

        self.frame_length = frame_length or self.get_frame_length(image_directory)  # Time in seconds until next frame, FPS independent
        self.time_until_next = self.frame_length
        self.pause = False

    def get_frame_length(self, image_directory):
        if os.path.exists(image_directory + "/meta.txt"):
            with open(image_directory + "/meta.txt", "r") as meta_file:
                data = meta_file.readline().strip()
                try:
                    return float(data)
                except ValueError:
                    return 0.25

        else:
            return 0.25

    def get_rect(self):
        self.frames[self.current_frame].get_rect()

    def next_frame(self):
        if not self.pause:
            if self.current_frame >= self.num_frames - 1:
                self.current_frame = 0
            else:
                self.current_frame += 1

    def tick(self, delta):
        self.time_until_next -= delta

        if self.time_until_next <= 0:
            self.next_frame()
            self.time_until_next = self.frame_length

    def render(self, screen, pos: Point, centered=False):
        self.frames[self.current_frame].render(screen, pos, centered)
