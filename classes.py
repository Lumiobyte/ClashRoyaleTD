import pygame
from dataclasses import dataclass
import math
import glob



@dataclass
class Point:
    """
    This dataclass is used to store coordinates. These coordinates may represent the location of an object, a point relevant to an object,
    or any other type of point. This reimplements operations like + - * / since one "position" object represents two numbers: an X and Y coordinate.
    """

    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        if isinstance(scalar, self.__class__):
            return Point(self.x * scalar.x, self.y * scalar.y)
        elif isinstance(scalar, tuple):
            return Point(self.x * scalar[0], self.y * scalar[1])
        else:
            return Point(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        if isinstance(scalar, self.__class__):
            return Point(self.x / scalar.x, self.y / scalar.y)
        elif isinstance(scalar, tuple):
            return Point(self.x / scalar[0], self.y / scalar[1])
        else:
            return Point(self.x / scalar, self.y / scalar)

    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def tuple(self):
        return (self.x, self.y)

    """
    Unused limit vars
    x_min_limit: int = None
    x_max_limit: int = None
    y_min_limit: int = None
    y_max_limit: int = None
    """


class Image:
    def __init__(self, filepath):
        self.image = pygame.image.load(filepath).convert_alpha()

        # Should support resizing image to any size inputted.

    def return_scaled_image(self):
        return self.image

    def get_rect(self):
        return self.image.get_rect()

    def render(self, screen, pos: Point, centered=False):
        if centered:
            pos -= Point(self.image.get_width() / 2, self.image.get_height() / 2)
        screen.blit(self.image, pos.tuple())


class AnimatedImage():
    def __init__(self, image_directory, frame_length):

        self.frames = []
        for filepath in glob.glob(f"{image_directory}/*.png"):
            self.frames.append(Image(filepath))

        self.num_frames = len(self.frames)
        self.current_frame = 0

        self.frame_length = frame_length
        self.time_until_next = self.frame_length
        self.pause = False

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

        if (self.time_until_next <= 0):
            self.next_frame()
            self.time_until_next = self.frame_length

    def render(self, screen, pos: Point, centered=False):
        self.frames[self.current_frame].render(screen, pos, centered)
